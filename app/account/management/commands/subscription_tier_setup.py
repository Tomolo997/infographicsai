from django.core.management.base import BaseCommand
from django.conf import settings
import stripe
from account.models import SubscriptionTier

stripe.api_key = settings.STRIPE_SECRET_KEY

class Command(BaseCommand):
    help = 'Creates subscription tiers in Stripe and Django'

    def handle(self, *args, **kwargs):
        # Define the tiers with limits
        tiers = [
            {
                'name': 'Free',
                'description': 'Free tier with basic features',
                'price': 0.00,
                'interval': 'month',
                'monthly_download_limit': 5,
                'ai_credits': 10,
                'is_free': True
            },
            {
                'name': 'Basic Monthly',
                'description': 'Basic subscription with 10 downloads/month and 100 AI credits',
                'price': 8.00,
                'interval': 'month',
                'monthly_download_limit': 10,
                'ai_credits': 100
            },
            {
                'name': 'Premium Monthly',
                'description': 'Premium subscription with 50 downloads/month and 200 AI credits',
                'price': 20.00,
                'interval': 'month',
                'monthly_download_limit': 50,
                'ai_credits': 200
            },
            {
                'name': 'Lifetime',
                'description': 'Unlimited downloads and 500 AI credits monthly',
                'price': 99.00,
                'interval': None,
                'monthly_download_limit': 999999,  # Effectively unlimited
                'ai_credits': 500
            }
        ]

        for tier in tiers:
            # Create or retrieve product in Stripe
            product = stripe.Product.create(
                name=tier['name'],
                description=tier['description']
            )

            # Create price in Stripe
            price_data = {
                'unit_amount': int(tier['price'] * 100),  # Convert to cents
                'currency': 'usd',
                'product': product.id,
            }

            if tier['interval']:
                price_data['recurring'] = {'interval': tier['interval']}

            price = stripe.Price.create(**price_data)

            # Create or update SubscriptionTier in Django
            defaults = {
                'stripe_price_id': price.id,
                'description': tier['description'],
                'price': tier['price'],
                'currency': 'USD',
                'monthly_download_limit': tier['monthly_download_limit'],
                'ai_credits': tier['ai_credits'],
            }
            
            if 'is_free' in tier:
                defaults['is_free'] = tier['is_free']

            subscription_tier, created = SubscriptionTier.objects.update_or_create(
                name=tier['name'],
                defaults=defaults
            )

            status = 'Created' if created else 'Updated'
            self.stdout.write(
                self.style.SUCCESS(f'{status} tier: {tier["name"]} (Price ID: {price.id})')
            )