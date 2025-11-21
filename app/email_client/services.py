from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from account.models import MagicLink
import resend


def send_verification_email(user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"http://localhost:3000/verify/?uid={uid}&token={token}"
    
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Account Verification"
    context = {"user": user, "verification_link": verification_link}
    html_content = render_to_string("account_verification_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return None


def send_magic_link_email(user):
    # Create a new MagicLink instance
    magic_link = MagicLink.objects.create(user=user)

    # Generate the verification link
    verification_link = f"{settings.FRONTEND_URL}/verify-magic-link?token={magic_link.token}"

    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Magic Link for Account Access"
    context = {
        "user": user,
        "verification_link": verification_link,
        "expiry_time": settings.MAGIC_LINK_EXPIRY_MINUTES,
    }
    html_content = render_to_string("magic_link_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return magic_link  # Return the magic_link object for testing or further processing
    except Exception as e:
        print(f"Error sending magic link email: {e}")
        return magic_link


def send_deletion_email(user):
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Help us improve: Why did you cancel your subscription?"
    context = {"user": user}
    html_content = render_to_string("subscription_deletion_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print(f"Error sending deletion email: {e}")
        return None


def send_subscription_success_email(subscription):
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Success! You have subscribed to our service"
    context = {"subscription": subscription}
    html_content = render_to_string("subscription_success_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [subscription.user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print(f"Error sending subscription success email: {e}")
        return None


def send_purchase_confirmation_email(user, credit_pack):
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Thank you for your credit purchase!"
    context = {
        "user": user,
        "credit_pack": credit_pack,
        "support_email": settings.SUPPORT_EMAIL,
        'account_url': settings.FRONTEND_URL + '/login'
    }
    html_content = render_to_string("credit_purchase_confirmation_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print(f"Error sending purchase confirmation email: {e}")
        return None


def send_payment_failed_email(subscription):
    """Send email notification when payment fails."""
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Action Required: Payment Failed for Your Subscription"
    context = {
        "subscription": subscription,
        "user": subscription.user,
        "dashboard_url": f"{settings.FRONTEND_URL}/dashboard/settings/",
        "support_email": settings.SUPPORT_EMAIL
    }
    html_content = render_to_string("payment_failed_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [subscription.user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print(f"Error sending payment failed email: {e}")
        return None


def send_subscription_cancelled_email(subscription):
    """Send confirmation email when a subscription is cancelled."""
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Your Subscription Has Been Cancelled"
    
    # Calculate the date when service will end
    end_date = subscription.end_date.strftime('%B %d, %Y') if subscription.end_date else "immediately"
    
    context = {
        "subscription": subscription,
        "user": subscription.user,
        "end_date": end_date,
        "reactivate_url": f"{settings.FRONTEND_URL}/dashboard/settings/",
        "feedback_url": f"{settings.FRONTEND_URL}/feedback/",
        "tier_name": subscription.tier.name
    }
    html_content = render_to_string("subscription_cancelled_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [subscription.user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print(f"Error sending subscription cancellation email: {e}")
        return None


def send_subscription_upgraded_email(subscription, old_tier_name):
    """Send confirmation email when a subscription is upgraded."""
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Your Subscription Has Been Upgraded!"
    
    context = {
        "subscription": subscription,
        "user": subscription.user,
        "old_tier": old_tier_name,
        "new_tier": subscription.tier.name,
        "new_ai_credits": subscription.tier.ai_credits,
        "new_download_limit": subscription.tier.monthly_download_limit,
        "dashboard_url": f"{settings.FRONTEND_URL}/dashboard/settings/",
    }
    html_content = render_to_string("subscription_upgraded_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [subscription.user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print(f"Error sending subscription upgrade email: {e}")
        return None


def send_subscription_reactivated_email(subscription):
    """Send confirmation email when a subscription is reactivated."""
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Your Subscription Has Been Reactivated"
    
    context = {
        "subscription": subscription,
        "user": subscription.user,
        "tier_name": subscription.tier.name,
        "ai_credits": subscription.tier.ai_credits,
        "download_limit": subscription.tier.monthly_download_limit,
        "dashboard_url": f"{settings.FRONTEND_URL}/dashboard/settings/",
        "support_email": settings.SUPPORT_EMAIL
    }
    html_content = render_to_string("subscription_reactivated_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [subscription.user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print(f"Error sending subscription reactivation email: {e}")
        return None


def send_credit_refill_notification(subscription):
    """Send notification when credits and downloads are refilled on billing date."""
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Your Credits and Downloads Have Been Refilled"
    
    context = {
        "subscription": subscription,
        "user": subscription.user,
        "tier_name": subscription.tier.name,
        "ai_credits": subscription.tier.ai_credits,
        "download_limit": subscription.tier.monthly_download_limit,
        "dashboard_url": f"{settings.FRONTEND_URL}/dashboard/",
    }
    html_content = render_to_string("credit_refill_notification_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [subscription.user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print(f"Error sending credit refill notification email: {e}")
        return None


def send_welcome_with_magic_link_email(user, magic_link_url, subscription=None):
    """
    Send a welcome email with magic link to a newly created user after Stripe payment.
    
    Args:
        user: The newly created user
        magic_link_url: The URL with the magic link token
        subscription: The user's subscription for details
    """
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Welcome to Ainfographic - Your Account is Ready!"
    
    context = {
        "user": user,
        "magic_link_url": magic_link_url,
        "subscription": subscription,
        "dashboard_url": f"{settings.FRONTEND_URL}/dashboard/",
        "support_email": settings.SUPPORT_EMAIL
    }
    
    html_content = render_to_string("welcome_with_magic_link_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print(f"Error sending welcome email with magic link: {e}")
        return None


def send_feedback_request_email(user):
    """Send a feedback request email to the user."""
    # Set Resend API key
    resend.api_key = settings.RESEND_API
    
    # Prepare email content
    email_subject = "Help us improve Ainfographic - Share your feedback!"
    
    context = {
        "user": user,
        "feedback_url": f"{settings.FRONTEND_URL}/dashboard/give-feedback/",
        "support_email": settings.SUPPORT_EMAIL
    }
    
    html_content = render_to_string("feedback_request_email.html", context)
    text_content = strip_tags(html_content)
    
    # Set up email parameters for Resend
    params = {
        "from": f"Ainfographic <{settings.DEFAULT_FROM_EMAIL}>",
        "to": [user.email],
        "subject": email_subject,
        "html": html_content,
        "text": text_content,
    }
    
    # Send email using Resend
    try:
        email_response = resend.Emails.send(params)
        print(email_response)
        return email_response
    except Exception as e:
        print(f"Error sending feedback request email: {e}")
        return None