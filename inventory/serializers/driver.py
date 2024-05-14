from rest_framework import serializers
from inventory.models.driver import Driver


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'contact_person', 'plate_number', 'phone_number', 'telegram_chat_id', 'email', 'description')
