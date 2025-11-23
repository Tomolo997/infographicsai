from infographs.models import AspectRatio, Infograph, Resolution, Template
from rest_framework import serializers


class InfographSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infograph
        fields = ['id', 'template', 'blog_url', 'image_url', 'resolution', 
                 'aspect_ratio', 'credits_used', 'created_at', 'updated_at', 'status']
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
    

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = ['id', 'name', 'image_url', 'aspect_ratio', 'created_at', 'updated_at']