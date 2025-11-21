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
        """Create the associated Account with initial credits"""
        if not hasattr(self, "account"):
            Account.objects.create(user=self)


class Account(models.Model):
    username = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    profile_picture_url = models.URLField(max_length=255, null=True, blank=True)
    credit_balance = models.PositiveIntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.email
