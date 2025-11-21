from django.core.management.base import BaseCommand
from django.utils import timezone
from account.models import Account, UserSubscription
from django.db import models

class Command(BaseCommand):
    help = 'Replenishes AI credits for active subscriptions'

    def handle(self, *args, **kwargs):
        # Get all active subscriptions
        active_subscriptions = UserSubscription.objects.filter(
            status='active'
        ).filter(
            models.Q(end_date__gte=timezone.now()) | 
            models.Q(is_lifetime=True)
        )

        count = 0
        for subscription in active_subscriptions:
            try:
                account = Account.objects.get(user=subscription.user)
                account.replenish_credits()
                count += 1
            except Account.DoesNotExist:
                continue

        self.stdout.write(
            self.style.SUCCESS(f'Successfully replenished credits for {count} accounts')
        )