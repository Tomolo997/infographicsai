import logging
import uuid

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

import stripe

import account

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
        super().save(*args, **kwargs)
        self._create_user_account()

    def _create_user_account(self):
        if not hasattr(self, "account"):
            Account.objects.create(user=self)


class Account(models.Model):
    username = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    profile_picture_url = models.URLField(max_length=255, null=True, blank=True)
    credit_balance = models.PositiveIntegerField(default=0)
    is_trial_user = models.BooleanField(default=True)


    def __str__(self):
        return self.user.email
    
    def fill_credits(self, credits: int):
        self.credit_balance += credits
        self.is_trial_user = False
        self.save()


class CreditPack(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    credits = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    stripe_price_id = models.CharField(max_length=255, null=True, blank=True)
    stripe_product_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_stripe_price_id(self):
        return self.stripe_price_id
    
class CreditPurchase(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    credit_pack = models.ForeignKey(CreditPack, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.user.email} purchased {self.quantity} credits from {self.credit_pack.name} for {self.price} at {self.created_at}"