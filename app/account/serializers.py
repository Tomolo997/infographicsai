from rest_framework import serializers

from email_client import services as email_services

from .models import Account, CustomUser


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
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def validate_email(self, value):
        existing_user = CustomUser.objects.filter(email=value).first()
        if existing_user:
            if existing_user.is_active:
                raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        if len(attrs['password1']) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        
        return attrs

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['email'].split('@')[0],  # Auto-generate username
        )
        user.set_password(validated_data['password1'])
        user.is_active = False  # User must verify email
        user.save()
        
        # Send verification email
        email_services.send_verification_email(user)
        
        return user