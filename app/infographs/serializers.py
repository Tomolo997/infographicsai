from infographs.models import (
    AspectRatio,
    Infograph,
    InfographType,
    Resolution,
    Template,
)
from rest_framework import serializers


class InfographSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infograph
        fields = ['id', 'template', 'blog_url', 'image_url', 'resolution', 
                 'aspect_ratio', 'credits_used', 'created_at', 'updated_at', 'status', 'type']
        read_only_fields = ['id', 'credits_used', 'created_at', 'updated_at', 'status']
    
    def validate_blog_url(self, value):
        """Custom validation for blog_url field"""
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("URL must start with http:// or https://")
        return value
    
    def validate_resolution(self, value):
        """Validate resolution is a valid choice"""
        valid_resolutions = [choice[0] for choice in Resolution.choices]
        if value not in valid_resolutions:
            raise serializers.ValidationError(f"Resolution must be one of: {valid_resolutions}")
        return value
    
    def validate_aspect_ratio(self, value):
        """Validate aspect ratio is a valid choice"""
        valid_aspect_ratios = [choice[0] for choice in AspectRatio.choices]
        if value not in valid_aspect_ratios:
            raise serializers.ValidationError(f"Aspect ratio must be one of: {valid_aspect_ratios}")
        return value
    
    def validate_type(self, value):
        """Validate infograph type is a valid choice"""
        valid_types = [choice[0] for choice in InfographType.choices]
        if value not in valid_types:
            raise serializers.ValidationError(f"Type must be one of: {valid_types}")
        return value
    

class TemplateSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    owner_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Template
        fields = ['id', 'name', 'image_url', 'is_public', 'is_owner', 'owner_email', 'created_at', 'updated_at', 'aspect_ratio']
    
    def get_is_owner(self, obj):
        """Check if the current user is the owner of this template"""
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return obj.account == request.user.account if obj.account else False
        return False
    
    def get_owner_email(self, obj):
        """Get the owner's email (for admin/debugging purposes)"""
        if obj.account and obj.account.user:
            return obj.account.user.email
        return "Public"
