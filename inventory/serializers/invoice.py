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

