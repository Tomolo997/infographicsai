from account.models import SubscriptionTier
from rest_framework import serializers

class SubscriptionTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionTier
        fields = ['id', 'name', 'stripe_price_id', 'description']