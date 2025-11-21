from django.db import models
from account import models as account_models
# Create your models here.

class SVGIcon(models.Model):
    title = models.CharField(max_length=255)
    cdn_url = models.URLField(max_length=500)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class VectorIcon(models.Model):
    title = models.CharField(max_length=255)
    cdn_url = models.URLField(max_length=500)
    file_format = models.CharField(max_length=10)  # AI, EPS, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class FlatIcon(models.Model):
    title = models.CharField(max_length=255)
    cdn_url = models.URLField(max_length=500)
    width = models.PositiveIntegerField(default=24)
    height = models.PositiveIntegerField(default=24)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Pattern(models.Model):
    title = models.CharField(max_length=255)
    cdn_url = models.URLField(max_length=500)
    file_format = models.CharField(max_length=20)  # AI, EPS, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class OutlineIcon(models.Model):
    title = models.CharField(max_length=255)
    cdn_url = models.URLField(max_length=500)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

