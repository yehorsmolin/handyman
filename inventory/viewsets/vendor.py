from rest_framework import viewsets, permissions
from rest_framework.response import Response
from inventory.models import Vendor
from inventory.serializers.vendor import VendorSerializer
from Handyman.permissions import IsVendorOrVendorStaff, IsVendor, IsAdminUser


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [IsAdminUser()]
    #     elif self.action in ['update', 'destroy']:
    #         return [IsAdminUser(), IsVendor()]
    #     elif self.action in ['list', 'retrieve', 'get']:
    #         return [IsAdminUser(), IsVendorOrVendorStaff]
    #     return super().get_permissions()

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            queryset = self.queryset.all()
        elif user.is_authenticated:
            queryset = self.queryset.filter(owner=user)
            if not queryset.exists():
                queryset = self.queryset.filter(staff=user)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

        serializer = VendorSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        if user.is_superuser or user == instance.owner or user in instance.staff.all():
            serializer = VendorSerializer(instance)
            return Response(serializer.data)
        return Response({'detail': 'You do not have permission to perform this action.'}, status=403)
