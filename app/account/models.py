from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
import uuid
import logging
from django.utils import timezone
from django.core.exceptions import ValidationError
import account.exceptions as account_exceptions

logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
import stripe
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None or kwargs.pop('is_new', False)
        skip_auto_subscription = kwargs.pop('skip_auto_subscription', False) 
        super().save(*args, **kwargs)

       
        if is_new:
            self._create_user_account()
            self._setup_free_subscription()

    def _create_user_account(self):
        """Create the associated Account with initial credits"""
        if not hasattr(self, 'account'):
            Account.objects.create(
                user=self,
                credit_balance=5
            )

    def _setup_free_subscription(self):
        """Set up the free tier subscription and Stripe customer"""
        try:
            # Create Stripe customer first
            stripe_customer = stripe.Customer.create(
                email=self.email,
                metadata={'user_id': str(self.id)}
            )

            # Get free tier
            free_tier = SubscriptionTier.objects.get(is_free=True)
            
            # Create subscription
            UserSubscription.objects.create(
                user=self,
                tier=free_tier,
                status='active',
                start_date=timezone.now(),
                stripe_customer_id=stripe_customer.id,
                is_lifetime=False
            )

        except SubscriptionTier.DoesNotExist:
            logger.error(
                "Free tier not found when creating user %s", 
                self.email,
                exc_info=True
            )
            raise
            
        except stripe.error.StripeError as e:
            logger.error(
                "Stripe error when creating customer for user %s: %s",
                self.email,
                str(e),
                exc_info=True
            )
            raise

        except Exception as e:
            logger.error(
                "Unexpected error setting up subscription for user %s: %s",
                self.email,
                str(e),
                exc_info=True
            )
            raise

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    profile_picture_url = models.URLField(max_length=255, null=True, blank=True)
    credit_balance = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    # Add download tracking
    monthly_downloads = models.IntegerField(default=0)
    last_download_reset = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email

    def reset_monthly_downloads_if_needed(self):
        """Reset download count if it's a new month"""
        now = timezone.now()
        if (
            now.year != self.last_download_reset.year
            or now.month != self.last_download_reset.month
        ):
            self.monthly_downloads = 0
            self.last_download_reset = now
            self.save()

    def get_active_subscription(self):
        """Get the user's active subscription"""
        try:
            return UserSubscription.objects.filter(user=self.user).last()
        except UserSubscription.DoesNotExist:
            return None

    def can_download(self):
        """Check if user can download based on their subscription"""
        self.reset_monthly_downloads_if_needed()
        subscription = self.get_active_subscription()

        if not subscription:
            return False, "No active subscription found."

        if self.monthly_downloads >= subscription.tier.monthly_download_limit:
            return False, "Monthly download limit reached."

        return True, "Download allowed."

    def increment_download(self):
        """Increment download count if allowed"""
        can_download, message = self.can_download()
        if not can_download:
            raise account_exceptions.DownloadForbidden(message)

        self.monthly_downloads += 1
        self.save()

    def can_use_ai_credits(self, credits_needed=1):
        """Check if user has enough AI credits"""
        if self.credit_balance < credits_needed:
            return False, "Insufficient AI credits."
        return True, "Sufficient credits available."

    def use_ai_credits(self, credits_needed=1):
        """Use AI credits if available"""
        can_use, message = self.can_use_ai_credits(credits_needed)
        if not can_use:
            raise ValidationError(message)

        self.credit_balance -= credits_needed
        self.save()

    def replenish_credits(self):
        """Replenish AI credits based on subscription tier"""
        subscription = self.get_active_subscription()
        if subscription:
            self.credit_balance = subscription.tier.ai_credits
            self.save()


class MagicLink(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)


class Suggestion(models.Model):
    CATEGORY_CHOICES = (
        ('general', 'General Feedback'),
        ('usability', 'Usability'),
        ('feature', 'Feature Request'),
        ('bug', 'Bug Report'),
        ('other', 'Other'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    suggestion_text = models.TextField()
    suggestion_title = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='general')
    rating = models.IntegerField(null=True, blank=True, help_text="User rating from 1-5")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion by {self.user.email} at {self.created_at}"
        
    def clean(self):
        if self.rating is not None and (self.rating < 1 or self.rating > 5):
            raise ValidationError("Rating must be between 1 and 5")


class SubscriptionTier(models.Model):
    name = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="USD")
    is_free = models.BooleanField(default=False)

    # Add limits
    monthly_download_limit = models.IntegerField(default=0)
    ai_credits = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, null=True, blank=True)
    tier = models.ForeignKey(SubscriptionTier, on_delete=models.PROTECT, null=True)
    status = models.CharField(max_length=50)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    billing_cycle_anchor = models.DateTimeField(null=True, blank=True)
    is_lifetime = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Replenish credits when new subscription is created
            account = Account.objects.get(user=self.user)
            account.replenish_credits()

    def __str__(self):
        return f"{self.user.email} - {self.tier}"
