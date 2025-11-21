from rest_framework import serializers
import json
from rest_framework import serializers
from .models import InfoGraph


class InfoRequestSerializer(serializers.Serializer):
    url = serializers.CharField(required=True)
    language=  serializers.CharField(required=True)


class InfoGraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoGraph
        fields = ['id', 'uuid', 'title', 'content', 'width', 'height', 'created_at', 'updated_at', 'background_color', 'preview_image_url']
        read_only_fields = ['id', 'uuid', 'created_at', 'updated_at']


    def validate(self, data):
        # Add validation for width and height
        if data.get('width', 0) <= 0:
            raise serializers.ValidationError("Width must be greater than 0")
        if data.get('height', 0) <= 0:
            raise serializers.ValidationError("Height must be greater than 0")
        return data
    
    def create(self, validated_data):
        # Get account from context
        account = self.context.get('account')
        if not account:
            raise serializers.ValidationError("Account is required for creating an infographic")
        # Set is_saved to True for all newly created infographics
        return InfoGraph.objects.create(account=account, is_saved=True, **validated_data)

    def update(self, instance, validated_data):
        # Don't modify the account during update
        for attr, value in validated_data.items():
            if attr != 'account':  # Skip account to avoid overwriting it
                setattr(instance, attr, value)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert UUID to string for JSON serialization
        representation['uuid'] = str(instance.uuid)
        return representation
    



class InfoGraphListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoGraph
        fields = ['id', 'uuid', 'title', 'width', 'height', 'preview_image_url', 'content', 'background_color']
    