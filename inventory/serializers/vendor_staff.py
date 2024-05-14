from rest_framework import serializers
from django.contrib.auth.models import User
from inventory.models.vendor_staff import VendorStaff


class VendorStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorStaff
        fields = ['id', 'user', 'contact_person', 'phone_number', 'telegram_chat_id', 'email', 'description', 'owner']


class VendorStaffReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorStaff
        fields = ['id', 'contact_person', 'phone_number', 'telegram_chat_id', 'email', 'description']
