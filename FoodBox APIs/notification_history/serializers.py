from rest_framework import serializers
from .models import NotiHistory


class NotiHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NotiHistory
        fields = '__all__'
