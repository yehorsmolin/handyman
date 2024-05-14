from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from inventory.models import Vendor, VendorStaff
from inventory.models.invoice import Invoice
from inventory.serializers.invoice import InvoiceSerializer, InvoiceReadOnlySerializer
from Handyman.permissions import IsVendorOrVendorStaff, IsVendor, IsAdminUser


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('supplier').all()
    serializer_class = InvoiceSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdminUser(), IsVendorOrVendorStaff]
        elif self.action in ['update', 'destroy']:
            return [IsAdminUser(), IsVendor()]
        elif self.action in ['list', 'retrieve', 'get']:
            return [IsAdminUser(), IsVendorOrVendorStaff]
        return super().get_permissions()

    def get_vendor_permission(self):
        if self.request.user.is_superuser:
            return permissions.AllowAny()
        return IsVendorOrVendorStaff

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            queryset = self.queryset.all()
        elif user.is_authenticated:
            try:
                vendor = Vendor.objects.get(owner=user)
                queryset = self.queryset.filter(owner=vendor)
            except Vendor.DoesNotExist:
                # Check if user is staff of any vendor
                staff_vendors = Vendor.objects.filter(staff=user)
                if staff_vendors.exists():
                    queryset = self.queryset.filter(owner__in=staff_vendors)
                else:
                    return Response({'detail': 'User is not associated with any vendor'}, status=403)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

        serializer = InvoiceReadOnlySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if user.is_superuser or user == instance.owner:
            serializer = InvoiceSerializer(instance)
            return Response(serializer.data)
        elif IsVendorOrVendorStaff().has_permission(request, self):
            try:
                vendor = VendorStaff.objects.get(user=user).owner
                if vendor == instance.owner:
                    serializer = InvoiceReadOnlySerializer(instance)
                    return Response(serializer.data)
            except VendorStaff.DoesNotExist:
                pass
        return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    def create(self, request, *args, **kwargs):
        user = request.user
        instance = None
        if user.is_superuser:
            return super().create(request, *args, **kwargs)
        elif IsVendorOrVendorStaff().has_permission(request, self):
            try:
                vendor = VendorStaff.objects.get(user=user).owner
                instance = Invoice(owner=vendor)  # Create instance with the correct owner
                if vendor == instance.owner:
                    return super().create(request, *args, **kwargs)
            except VendorStaff.DoesNotExist:
                pass
        return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    def update(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if user.is_superuser or user == instance.owner:
            return super().update(request, *args, **kwargs)
        elif IsVendorOrVendorStaff().has_permission(request, self):
            try:
                vendor = VendorStaff.objects.get(user=user).owner
                if vendor == instance.owner:
                    return super().update(request, *args, **kwargs)
            except VendorStaff.DoesNotExist:
                pass
        return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        instance = self.get_object()
        if user.is_superuser or user == instance.owner:
            return super().destroy(request, *args, **kwargs)
        return Response({'detail': 'You do not have permission to perform this action.'}, status=403)