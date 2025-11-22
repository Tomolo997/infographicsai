from django.db import models

from account.models import Account

# Create your models here.

class Resolution(models.TextChoices):
    ONE_K = '1K', '1K'
    TWO_K = '2K', '2K'
    FOUR_K = '4K', '4K'

class AspectRatio(models.TextChoices):
    NINE_ONE_SIX = '9/16', '9:16'
    ONE_ONE = '1/1', '1:1'
    FOUR_FIVE = '4/5', '4:5'
    SIXTEEN_NINE = '16/9', '16:9'
    TWENTY_ONE_NINE = '21/9', '21:9'
    THREE_TWO = '3/2', '3:2'
    FOUR_THREE = '4/3', '4:3'
    TWO_THREE = '2/3', '2:3'

class Infograph(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    template = models.ForeignKey('Template', on_delete=models.CASCADE, null=True, blank=True)
    blog_url = models.URLField(null=True, blank=True)
    blog_json = models.JSONField(null=True, blank=True) 
    image_url = models.URLField(null=True, blank=True) # Image URL from R2
    resolution = models.CharField(max_length=255, choices=Resolution.choices, default=Resolution.TWO_K)
    aspect_ratio = models.CharField(max_length=255, choices=AspectRatio.choices, default=AspectRatio.NINE_ONE_SIX)
    credits_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account.user.email} - {self.created_at}"



class Template(models.Model):
    name = models.CharField(max_length=255)
    image_url = models.URLField(null=True, blank=True)
    aspect_ratio = models.CharField(max_length=255, choices=AspectRatio.choices, default=AspectRatio.NINE_ONE_SIX)
    description_json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)