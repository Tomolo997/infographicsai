# your_app/management/commands/create_free_tier.py
from django.core.management.base import BaseCommand
from account.models import SubscriptionTier

class Command(BaseCommand):
    help = 'Creates the free subscription tier'

    def handle(self, *args, **kwargs):
        free_tier, created = SubscriptionTier.objects.get_or_create(
            name='Free',
            defaults={
                'description': 'Free tier with basic features',
                'price': 0,
                'monthly_download_limit': 5,
                'ai_credits': 10,
                'is_free': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created free tier'))
        else:
            self.stdout.write(self.style.SUCCESS('Free tier already exists'))