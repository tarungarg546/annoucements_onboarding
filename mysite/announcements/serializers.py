from rest_framework import serializers
from .models import AnnouncementDeliveryStatus


class AnnouncementDeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementDeliveryStatus
        fields = ('announcement', 'user', 'status_last_update_time', 'status')
