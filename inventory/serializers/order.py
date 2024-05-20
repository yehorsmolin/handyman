from rest_framework import serializers

from inventory.models.order import Order
from inventory.serializers.product import ProductReadOnlySerializer


class OrderReadOnlySerializer(serializers.ModelSerializer):
    order_products = ProductReadOnlySerializer(many=True, read_only=True)
    owner = serializers.HiddenField(default=0)

    class Meta:
        model = Order
        fields = ('uuid',
                  'owner',
                  'order_products',
                  'display_number',
                  'created_at',
                  'updated_at')

    @property
    def owner(self):
        from inventory.serializers.vendor import VendorSerializer
        owner = VendorSerializer(read_only=True)
        return owner


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('uuid', 'owner', 'order_products', 'display_number', 'created_at', 'updated_at')

