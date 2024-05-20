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
        fields = ('id', 'title', 'category', 'storage', 'grade', 'color', 'price',
                  'status', 'supplier', 'invoice', 'imei', 'owner')
