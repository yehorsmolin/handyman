from rest_framework import serializers
from inventory.models.invoice import Invoice
from inventory.serializers.supplier import SupplierSerializer
from inventory.serializers.vendor import VendorSerializer


class InvoiceReadOnlySerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)
    owner = VendorSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = (
            'uuid',
            'invoice_number',
            'owner',
            'supplier',
            'products',
            'created_at',
            'updated_at')

    @property
    def fields(self):
        from inventory.serializers.product import ProductReadOnlySerializer
        fields = super().fields
        fields['products'] = ProductReadOnlySerializer(many=True, read_only=True)
        return fields


class InvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ('uuid', 'invoice_number', 'owner', 'supplier', 'products', 'created_at', 'updated_at')

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
            raise serializers.ValidationError("You do not have permission to create invoices.")

        # Set the Vendor as the owner of the invoice
        validated_data['owner_id'] = vendor_id
        return super().create(validated_data)