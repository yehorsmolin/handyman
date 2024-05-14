from rest_framework import serializers

from inventory.models.supplier import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = (
            'id', 'title', 'contact_person', 'email', 'website', 'phone_number', 'description',
            'billing_address', 'shipping_address',
                  )
