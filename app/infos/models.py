# models.py
import uuid
from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from account import models as account_models
from django.core.validators import URLValidator


class InfoGraph(models.Model):
    title = models.CharField(max_length=255)
    content = models.JSONField(encoder=DjangoJSONEncoder, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    account = models.ForeignKey(
        account_models.Account, on_delete=models.CASCADE, related_name="infographs"
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    width = models.IntegerField(default=1024)
    height = models.IntegerField(default=1024)
    background_color = models.CharField(default="#FFFFFF", max_length=20)
    preview_image_url = models.URLField(
        max_length=500,
        validators=[URLValidator(schemes=["https"])],
        blank=True,
        default="https://ainfographic.com/generated_images/preview.png",
        help_text="HTTPS URL for the preview image",
    )
    is_template=models.BooleanField(default=False)
    is_saved=models.BooleanField(default=False)
    TEMPLATE_TYPE_CHOICES = [
        ('letter', 'Letter'),
        ('normal', 'Normal'),
    ]
    template_type = models.CharField(max_length=255, default="normal", choices=TEMPLATE_TYPE_CHOICES)

    def __str__(self):
        return f"{self.title} - {self.account}"

    class Meta:
        verbose_name = "InfoGraph"
        verbose_name_plural = "InfoGraphs"
        ordering = ["-created_at"]

    @property
    def get_json(self):
        return self.content

    def set_json(self, data):
        self.content = data
        self.save()



class MediaUpload(models.Model):
    account = models.ForeignKey(account_models.Account, on_delete=models.CASCADE, related_name='media_uploads')
    url = models.URLField()
    filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50)  # For storing mime type
    file_size = models.IntegerField()  # Size in bytes

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.filename}"