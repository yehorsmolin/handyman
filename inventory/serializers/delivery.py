from rest_framework import serializers
from inventory.models.delivery import Delivery


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = ['title',
                  'description',
                  'order',
                  'driver',
                  'pick_up_address',
                  'delivery_address',
                  'boxes',
                  'dimensions',
                  'weight',
                  'owner',
                  'is_active']
