from rest_framework import serializers

from inventory.models.product import Product
from inventory.serializers.category import CategorySerializer
from inventory.serializers.grade import GradeSerializer
from inventory.serializers.storage import StorageSerializer
from inventory.serializers.color import ColorSerializer
from inventory.serializers.status import StatusSerializer
from inventory.serializers.supplier import SupplierSerializer
from inventory.serializers.invoice import InvoiceSerializer
from inventory.serializers.vendor import VendorSerializer


class ProductReadOnlySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    storage = StorageSerializer(read_only=True)
    grade = GradeSerializer(read_only=True)
    color = ColorSerializer(read_only=True)
    status = StatusSerializer(read_only=True)
    supplier = SupplierSerializer(read_only=True)
    invoice = InvoiceSerializer(read_only=True)
    owner = VendorSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'category',
            'storage',
            'grade',
            'price',
            'color',
            'status',
            'supplier',
            'invoice',
            'owner',
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'storage', 'grade', 'price', 'status', 'supplier', 'invoice', 'imei', 'owner')

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
            raise serializers.ValidationError("You do not have permission to create products.")

        # Set the Vendor as the owner of the product
        validated_data['owner_id'] = vendor_id
        return super().create(validated_data)
