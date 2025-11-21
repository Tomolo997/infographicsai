from .models import Account
from rest_framework import serializers
from .models import CustomUser, SubscriptionTier
from email_client import services as email_services

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'groups', 'user_permissions','is_active', 'is_staff', 'date_joined')

# Serializers define the API representation.
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'profile_picture_url', 'credit_balance']


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        
        email_services.send_verification_email(user)
        return user
    

class SubscriptionTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionTier
        fields = [
            'id',
            'name',
            'description',
            'price',
            'currency',
            'monthly_download_limit',
            'ai_credits',
        ]