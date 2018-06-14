from rest_framework import serializers
from .models import Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('announcement', 'user', 'status_last_update_time', 'status')
