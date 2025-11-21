# serializers.py
from rest_framework import serializers
from .models import SVGIcon, VectorIcon

class SVGIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = SVGIcon
        fields = ['id', 'title', 'cdn_url', 'width', 'height', 'created_at']
        read_only_fields = ['created_at']

class VectorIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorIcon
        fields = ['id', 'title', 'cdn_url', 'file_format', 'created_at']
        read_only_fields = ['created_at']