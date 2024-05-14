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

    def create(self, validated_data):
        # Extract the Vendor ID based on the user's role
        user = self.context['request'].user
        if user.is_superuser or user.is_vendor:
            # If user is a vendor, use the vendor's ID as the owner
            vendor_id = user.vendor.id
        elif user.is_vendor_staff:
            # If user is a vendor staff, use the associated vendor's ID as the owner
            vendor_id = user.vendorstaff.owner.id
        else:
            # If user does not have appropriate permissions, raise an error
            raise serializers.ValidationError("You do not have permission to create orders.")

        # Set the Vendor as the owner of the order
        validated_data['owner_id'] = vendor_id
        return super().create(validated_data)
