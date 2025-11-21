from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account.models import SubscriptionTier, CustomUser, UserSubscription, MagicLink
import stripe
import logging
from django.utils import timezone
from django.shortcuts import get_object_or_404
from email_client import services as email_services
from account.serializers import SubscriptionTierSerializer
import os
from django.db import models
from rest_framework import status
from rest_framework.permissions import AllowAny

logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = os.environ.get("ENDPOINT_SECRET")


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")
    event = None

    logger.debug("Received webhook - Processing started")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        logger.error(f"Invalid payload: {str(e)}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {str(e)}")
        return HttpResponse(status=400)

    logger.info(f"Webhook event type: {event['type']}")

    try:
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            customer_email = session["customer_email"]
            metadata = session.get("metadata", {})
            user_id = metadata.get("user_id")

            if not customer_email:
                customer_email = session["customer_details"]["email"]

            user_is_new = False
            # Try to get existing user
            user = None
            if user_id:
                try:
                    user = CustomUser.objects.get(id=user_id)
                except CustomUser.DoesNotExist:
                    logger.warning(f"User with ID {user_id} not found")

            if not user:
                try:
                    user = CustomUser.objects.get(email=customer_email)

                except CustomUser.DoesNotExist:
                    # Create a new user if no user found
                    logger.info(f"Creating new user for email: {customer_email}")
                    # Generate a random password for the user
                    user = CustomUser.objects.create_user(
                        email=customer_email,
                        username=customer_email.split("@")[
                            0
                        ],  # Use part before @ as username
                        is_active=True,
                    )
                    UserSubscription.objects.filter(
                        user=user, tier__is_free=True
                    ).delete()

                    user_is_new = True

                    # Create a magic link for automatic login
                    if user_is_new:
                        magic_link = MagicLink.objects.create(user=user)
                        logger.info(
                            f"Created magic link for auto-login for new user: {user.email}"
                        )

                    logger.info(f"New user created with email: {customer_email}")

            # Handle one-time payments (lifetime subscriptions)
            if session["mode"] == "payment":
                payment_intent = session["payment_intent"]
                tier_price_id = session["metadata"].get("tier_id")

                try:
                    selected_tier = SubscriptionTier.objects.get(id=tier_price_id)
                except SubscriptionTier.DoesNotExist:
                    logger.error(f"Tier not found for price_id: {tier_price_id}")
                    return HttpResponse(status=400)

                user_subscription = UserSubscription.objects.create(
                    user=user,
                    tier=selected_tier,
                    status="active",
                    start_date=timezone.now(),
                    is_lifetime=True,
                )

            # Handle regular subscriptions
            else:
                subscription_id = session["subscription"]
                subscription = stripe.Subscription.retrieve(subscription_id)
                tier_price_id = subscription["items"]["data"][0]["price"]["id"]

                try:
                    selected_tier = SubscriptionTier.objects.get(
                        stripe_price_id=tier_price_id
                    )
                except SubscriptionTier.DoesNotExist:
                    logger.error(f"Tier not found for price_id: {tier_price_id}")
                    return HttpResponse(status=400)

                # Check for and update any existing subscriptions
                existing_sub = UserSubscription.objects.filter(
                    user=user, status__in=["active"]
                ).first()

                if existing_sub:
                    existing_sub.status = "canceled"
                    existing_sub.end_date = timezone.now()
                    existing_sub.save()

                user_subscription = UserSubscription.objects.create(
                    user=user,
                    stripe_customer_id=session["customer"],
                    stripe_subscription_id=subscription_id,
                    tier=selected_tier,
                    status=subscription["status"],
                    start_date=timezone.datetime.fromtimestamp(
                        subscription["current_period_start"]
                    ),
                    end_date=timezone.datetime.fromtimestamp(
                        subscription["current_period_end"]
                    ),
                    billing_cycle_anchor=timezone.datetime.fromtimestamp(
                        subscription["billing_cycle_anchor"]
                    ),
                )

            # Replenish credits based on new subscription
            account = user.account
            account.credit_balance = selected_tier.ai_credits
            account.monthly_downloads = 0  # Reset download count
            account.last_download_reset = timezone.now()
            account.save()
            if not user_is_new:
                email_services.send_subscription_success_email(
                    subscription=user_subscription
                )
            if user_is_new:
                magic_link_url = f"{settings.FRONTEND_URL}/verify-magic-link?token={magic_link.token}"
                email_services.send_welcome_with_magic_link_email(
                    user=user,
                    magic_link_url=magic_link_url,
                    subscription=user_subscription,
                )
            logger.info(f"Subscription created successfully for user: {user.email}")

        elif event["type"] == "invoice.payment_succeeded":
            subscription_id = event["data"]["object"]["subscription"]
            user_subscription = UserSubscription.objects.get(
                stripe_subscription_id=subscription_id
            )

            # Update tier in case of plan change
            new_price_id = event["data"]["object"]["lines"]["data"][0]["price"]["id"]
            new_tier = SubscriptionTier.objects.get(stripe_price_id=new_price_id)

            user_subscription.tier = new_tier
            user_subscription.end_date = timezone.datetime.fromtimestamp(
                event["data"]["object"]["lines"]["data"][0]["period"]["end"]
            )
            user_subscription.save()

            # Explicitly log and handle recharge
            logger.info(
                f"Resetting downloads and replenishing credits for user {user_subscription.user.email} on billing cycle"
            )
            account = user_subscription.user.account
            account.credit_balance = new_tier.ai_credits
            account.monthly_downloads = 0  # Reset download count
            account.last_download_reset = timezone.now()
            account.save()

            logger.info(f"Payment succeeded for subscription: {subscription_id}")

        elif event["type"] == "customer.subscription.updated":
            try:
                subscription = event["data"]["object"]
                tier_price_id = subscription["items"]["data"][0]["price"]["id"]
                subscription_id = subscription["id"]
                metadata = subscription.get("metadata", {})
                is_upgrade = metadata.get("is_upgrade") == "true"
                user_id = metadata.get("user_id")

                if metadata.get("cancellation_requested") == "true":
                    logger.info(
                        f"Skipping subscription update for cancellation: {subscription['id']}"
                    )
                    return HttpResponse(status=200)

                try:
                    selected_tier = SubscriptionTier.objects.get(
                        stripe_price_id=tier_price_id
                    )

                    # If it's an upgrade, find the subscription by user_id
                    if is_upgrade and user_id:
                        user = CustomUser.objects.get(id=user_id)
                        user_subscription = UserSubscription.objects.filter(
                            user=user, status__in=["active", "trialing"]
                        ).first()

                        if not user_subscription:
                            # Create new subscription if none exists
                            user_subscription = UserSubscription.objects.create(
                                user=user,
                                stripe_subscription_id=subscription_id,
                                stripe_customer_id=subscription["customer"],
                                tier=selected_tier,
                                status=subscription["status"],
                                start_date=timezone.datetime.fromtimestamp(
                                    subscription["current_period_start"],
                                    tz=timezone.utc,
                                ),
                                end_date=timezone.datetime.fromtimestamp(
                                    subscription["current_period_end"], tz=timezone.utc
                                ),
                            )
                    else:
                        # Regular update - find by subscription_id
                        user_subscription = UserSubscription.objects.get(
                            stripe_subscription_id=subscription_id
                        )

                    old_status = user_subscription.status
                    new_status = subscription["status"]

                    # Update subscription details
                    user_subscription.status = new_status
                    user_subscription.tier = selected_tier
                    user_subscription.end_date = timezone.datetime.fromtimestamp(
                        subscription["current_period_end"], tz=timezone.utc
                    )
                    user_subscription.save()

                    # Handle account updates based on status change
                    if old_status != new_status or is_upgrade:
                        logger.info(f"Status changed from {old_status} to {new_status}")
                        account = user_subscription.user.account

                        if new_status in ["incomplete_expired", "canceled", "unpaid"]:
                            account.credit_balance = 5
                        elif new_status == "active":
                            account.credit_balance = selected_tier.ai_credits
                            account.monthly_downloads = 0
                            account.last_download_reset = timezone.now()

                        account.save()

                    if is_upgrade:
                        old_tier_name = metadata.get("old_tier_name", "previous plan")
                        email_services.send_subscription_upgraded_email(
                            subscription=user_subscription, old_tier_name=old_tier_name
                        )
                    else:
                        logger.info(
                            f"Subscription updated: {subscription_id}, Status: {new_status}"
                        )

                except SubscriptionTier.DoesNotExist:
                    logger.error(f"Tier not found for price_id: {tier_price_id}")
                    return HttpResponse(status=400)
                except UserSubscription.DoesNotExist:
                    logger.error(f"Subscription not found: {subscription_id}")
                    return HttpResponse(status=400)
                except CustomUser.DoesNotExist:
                    logger.error(f"User not found: {user_id}")
                    return HttpResponse(status=400)

            except Exception as e:
                logger.error(f"Error processing subscription update: {str(e)}")
                return HttpResponse(status=400)

        elif event["type"] == "invoice.payment_failed":
            subscription_id = event["data"]["object"]["subscription"]
            user_subscription = UserSubscription.objects.get(
                stripe_subscription_id=subscription_id
            )
            user_subscription.status = "past_due"
            user_subscription.save()

            # Optionally send email notification
            email_services.send_payment_failed_email(subscription=user_subscription)
            logger.warning(f"Payment failed for subscription: {subscription_id}")

        elif event["type"] == "customer.subscription.deleted":
            subscription = event["data"]["object"]
            user_subscription = UserSubscription.objects.get(
                stripe_subscription_id=subscription["id"]
            )
            user_subscription.status = "canceled"
            user_subscription.end_date = timezone.now()
            user_subscription.save()

            # Reset account to free tier limits
            account = user_subscription.user.account
            account.credit_balance = 5  # Reset to default
            account.save()

            logger.info(f"Subscription deleted: {subscription['id']}")

        elif event["type"] == "customer.created":
            customer = event["data"]["object"]
            customer_email = customer.get("email")
            customer_id = customer.get("id")

            logger.info(
                f"New Stripe customer created: {customer_id} with email: {customer_email}"
            )

            # Check if user already exists with this email
            try:
                user = CustomUser.objects.get(email=customer_email)
                user_subscription = UserSubscription.objects.filter(user=user).first()
                # Update the user's stripe customer ID if needed

                if (
                    not hasattr(user_subscription, "stripe_customer_id")
                    or not user_subscription.stripe_customer_id
                ):
                    logger.info(
                        f"Updating existing user with Stripe customer ID: {customer_id}"
                    )
                    # This would depend on your model structure
                    # If stripe_customer_id is stored in UserSubscription, you might not need this
                    user_subscription.stripe_customer_id = customer_id
                    user_subscription.save()
            except CustomUser.DoesNotExist:
                logger.info(
                    f"No existing user found for new Stripe customer: {customer_email}"
                )
                # We don't create a user here as that's handled in checkout.session.completed
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return HttpResponse(status=400)

    return HttpResponse(status=200)


stripe.api_key = settings.STRIPE_SECRET_KEY


class PublicCheckoutSessionView(APIView):
    permission_classes = []  # No authentication required

    def post(self, request):
        # Get the selected tier
        selected_tier_id = request.data.get("tier_id")
        coupon_code = request.data.get("coupon_code")
        if coupon_code and settings.DEBUG:
            coupon_code = "oS5eyDjj"
        if coupon_code and not settings.DEBUG:
            coupon_code = 'iMB0FrXJ'
        if not selected_tier_id:
            return Response({"error": "Please select a subscription tier"}, status=400)

        selected_tier = get_object_or_404(SubscriptionTier, id=selected_tier_id)

        if selected_tier.is_free:
            return Response({"url": settings.FRONTEND_URL + "/signup", "is_free": True})

        try:
            # Create checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": selected_tier.stripe_price_id,
                        "quantity": 1,
                    }
                ],
                mode=(
                    "subscription"
                    if not selected_tier.name == "Lifetime"
                    else "payment"
                ),
                success_url=settings.FRONTEND_URL + "/subscribe/success",
                cancel_url=settings.FRONTEND_URL + "/",
                metadata={"tier_id": selected_tier.id},
                discounts=[{"coupon": coupon_code}] if coupon_code and selected_tier.name == "Lifetime" else None,
            )

            return Response({"url": checkout_session.url})
        except Exception as e:
            logger.error(f"Error creating checkout session: {str(e)}")
            return Response({"error": "Unable to create checkout session"}, status=500)


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the selected tier
        selected_tier_id = request.data.get("tier_id")
        if not selected_tier_id:
            return Response({"error": "Please select a subscription tier"}, status=400)

        selected_tier = get_object_or_404(SubscriptionTier, id=selected_tier_id)

        # Check if user already has an active subscription
        existing_subscription = UserSubscription.objects.filter(
            user=request.user,
            status="active",
            tier__is_free=False,  # Don't block if they only have free tier
        ).first()

        if existing_subscription:
            return Response(
                {
                    "error": "You already have an active subscription. Please upgrade instead."
                },
                status=400,
            )

        try:
            # Create checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": selected_tier.stripe_price_id,
                        "quantity": 1,
                    }
                ],
                mode=(
                    "subscription"
                    if not selected_tier.name == "Lifetime"
                    else "payment"
                ),
                success_url=settings.FRONTEND_URL
                + "/dashboard/settings/?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.FRONTEND_URL + "/dashboard/settings/",
                customer_email=request.user.email,
                metadata={"tier_id": selected_tier.id, "user_id": request.user.id},
                subscription_data=None,
                allow_promotion_codes=True  
            )

            return Response({"id": checkout_session.id, "url": checkout_session.url})

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class UpgradeSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_tier_id = request.data.get("tier_id")
        if not new_tier_id:
            return Response({"error": "Please select a subscription tier"}, status=400)

        new_tier = get_object_or_404(SubscriptionTier, id=new_tier_id)

        # Get current subscription
        current_subscription = UserSubscription.objects.filter(
            user=request.user,
            status__in=["active", "trialing"],  # Only get active subscriptions
        ).first()

        if not current_subscription:
            return Response({"error": "No active subscription found"}, status=400)

        if current_subscription.is_lifetime:
            return Response(
                {"error": "Cannot upgrade lifetime subscription"}, status=400
            )

        try:
            # First cancel the current subscription at period end
            if not current_subscription.tier.is_free:
                stripe.Subscription.modify(
                    current_subscription.stripe_subscription_id,
                    cancel_at_period_end=True,
                )

            # Store the old tier name before upgrading
            old_tier_name = current_subscription.tier.name

            # Create a subscription upgrade checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": new_tier.stripe_price_id,
                        "quantity": 1,
                    }
                ],
                mode="subscription",
                success_url=settings.FRONTEND_URL
                + "/dashboard/settings/?upgrade_success=true",
                cancel_url=settings.FRONTEND_URL + "/dashboard/settings/",
                customer=current_subscription.stripe_customer_id,
                metadata={
                    "user_id": str(request.user.id),
                    "customer_email": request.user.email,
                    "upgrade_to_tier": str(new_tier_id),
                    "is_upgrade": "true",
                },
                subscription_data={
                    "trial_period_days": None,  # No trial for upgrades
                    "metadata": {
                        "user_id": str(request.user.id),
                        "is_upgrade": "true",
                    },
                },
            )

            return Response({"id": checkout_session.id, "url": checkout_session.url})

        except Exception as e:
            logger.error(f"Error creating upgrade session: {str(e)}")
            return Response({"error": str(e)}, status=400)


class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription = UserSubscription.objects.filter(
            user=request.user, status="active"
        ).first()

        if not subscription:
            return Response({"error": "No active subscription found"}, status=400)

        if subscription.is_lifetime:
            return Response(
                {"error": "Cannot cancel lifetime subscription"}, status=400
            )

        try:
            # Cancel at period end
            stripe.Subscription.modify(
                subscription.stripe_subscription_id,
                cancel_at_period_end=True,
                metadata={"cancellation_requested": "true"},
            )
            subscription.status = "canceling"
            subscription.save()

            email_services.send_subscription_cancelled_email(subscription=subscription)

            return Response(
                {
                    "message": "Subscription will be canceled at the end of the billing period"
                }
            )

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class ReactivateSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription = UserSubscription.objects.filter(
            user=request.user, status="canceling"
        ).first()

        if not subscription:
            return Response({"error": "No subscription to reactivate"}, status=400)

        try:
            # Remove the cancellation status
            stripe.Subscription.modify(
                subscription.stripe_subscription_id, cancel_at_period_end=False
            )

            subscription.status = "active"
            subscription.save()

            email_services.send_subscription_reactivated_email(
                subscription=subscription
            )

            return Response({"message": "Subscription reactivated successfully"})

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class GetSubscriptionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscription = (
            UserSubscription.objects.filter(user=request.user)
            .select_related("tier")
            .last()
        )

        if not subscription:
            return Response({"has_subscription": False, "subscription": None})

        return Response(
            {
                "has_subscription": True,
                "subscription": {
                    "tier_name": subscription.tier.name,
                    "status": subscription.status,
                    "end_date": subscription.end_date,
                    "is_lifetime": subscription.is_lifetime,
                    "monthly_download_limit": subscription.tier.monthly_download_limit,
                    "ai_credits": subscription.tier.ai_credits,
                    "downloads_remaining": subscription.tier.monthly_download_limit
                    - request.user.account.monthly_downloads,
                    "credits_remaining": request.user.account.credit_balance,
                },
            }
        )


class AvailableUpgradesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get user's current subscription
            current_subscription = UserSubscription.objects.filter(
                user=request.user
            ).last()
            # Get current tier's price for comparison
            current_price = current_subscription.tier.price

            # Get all tiers that are more expensive than current tier
            # Exclude lifetime plans if user has a monthly subscription and vice versa
            available_tiers = (
                SubscriptionTier.objects.filter(price__gt=current_price)
                .order_by("price")
            )

            serializer = SubscriptionTierSerializer(available_tiers, many=True)

            return Response(
                {
                    "current_tier": SubscriptionTierSerializer(
                        current_subscription.tier
                    ).data,
                    "available_upgrades": serializer.data,
                    "current_usage": {
                        "downloads_used": request.user.account.monthly_downloads,
                        "downloads_limit": current_subscription.tier.monthly_download_limit,
                        "credits_remaining": request.user.account.credit_balance,
                        "credits_total": current_subscription.tier.ai_credits,
                    },
                }
            )
        except UserSubscription.DoesNotExist:
            return Response(
                {"error": "No active subscription found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class AllSubscriptionTiersView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Returns all available subscription tiers.
        """
        try:
            # Get all subscription tiers ordered by price
            tiers = SubscriptionTier.objects.all().order_by("price")

            # Separate tiers into categories
            free_tiers = [tier for tier in tiers if tier.is_free]
            monthly_tiers = [
                tier
                for tier in tiers
                if not tier.is_free and "monthly" in tier.name.lower()
            ]
            lifetime_tiers = [
                tier
                for tier in tiers
                if not tier.is_free and "lifetime" in tier.name.lower()
            ]
            other_tiers = [
                tier
                for tier in tiers
                if not tier.is_free
                and "monthly" not in tier.name.lower()
                and "lifetime" not in tier.name.lower()
            ]

            # Serialize the data
            serializer = SubscriptionTierSerializer(tiers, many=True)

            return Response(
                {
                    "all_tiers": serializer.data,
                    "categories": {
                        "free": SubscriptionTierSerializer(free_tiers, many=True).data,
                        "monthly": SubscriptionTierSerializer(
                            monthly_tiers, many=True
                        ).data,
                        "lifetime": SubscriptionTierSerializer(
                            lifetime_tiers, many=True
                        ).data,
                        "other": SubscriptionTierSerializer(
                            other_tiers, many=True
                        ).data,
                    },
                }
            )
        except Exception as e:
            logger.error(f"Error retrieving subscription tiers: {str(e)}")
            return Response(
                {"error": "Error retrieving subscription tiers"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
