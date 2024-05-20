from rest_framework import serializers
from django.contrib.auth.models import User
from inventory.models.vendor import Vendor


# class CustomOwnerField(e2e.PrimaryKeyRelatedField):
#     def get_default(self):
#         user = self.context['request'].user
#         if user.is_authenticated and user.is_superuser:
#             return None  # If superadmin or any admin, don't set default
#         return e2e.CurrentUserDefault()


class VendorSerializer(serializers.ModelSerializer):
    # owner = CustomOwnerField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Vendor
        fields = (
            'id', 'title', 'contact_person', 'email', 'website', 'phone_number', 'description',
            'billing_address', 'shipping_address', 'owner', 'verified', 'is_active', 'staff'
                  )
