from django.core.management.base import BaseCommand
from account.models import CustomUser, Suggestion
from email_client.services import send_feedback_request_email
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Sends feedback request emails to all users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually sending emails',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Get all active users
        users = CustomUser.objects.filter(is_active=True)
        total_users = users.count()
        
        self.stdout.write(f"Found {total_users} active users")
        
        if dry_run:
            self.stdout.write("Running in dry-run mode. No emails will be sent.")
        
        for user in users:
            try:
                # Check if user has already submitted feedback recently (within last 30 days)
                # Only check for recent feedback for the last 70 users
                users_to_check = CustomUser.objects.filter(is_active=True).order_by('-date_joined')[:70]
                recent_feedback = False
                if user in users_to_check:
                    recent_feedback = Suggestion.objects.filter(
                        user=user,
                        created_at__gte=timezone.now() - timezone.timedelta(days=30)
                    ).exists()
                
                if recent_feedback:
                    self.stdout.write(f"Skipping {user.email} - already submitted feedback recently")
                    continue
                
                if not dry_run:
                    send_feedback_request_email(user)
                    self.stdout.write(f"Sent feedback request to {user.email}")
                else:
                    self.stdout.write(f"Would send feedback request to {user.email}")
                    
            except Exception as e:
                logger.error(f"Error sending feedback request to {user.email}: {str(e)}")
                self.stdout.write(self.style.ERROR(f"Error sending to {user.email}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS("Feedback request process completed")) 