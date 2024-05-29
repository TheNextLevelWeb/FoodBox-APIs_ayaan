from rest_framework import serializers
from .models import TrackOrder


class TrackOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TrackOrder
        fields = ['order_number', 'status', 'created_at', 'updated_at']


class TrackOrderCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TrackOrder
        fields = ['order_number', 'status']


class TrackOrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackOrder
        fields = ['status']
