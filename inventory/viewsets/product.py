from rest_framework import viewsets
from rest_framework.response import Response
from inventory.models.product import Product
from inventory.models.vendor import Vendor
from inventory.serializers import ProductSerializer, ProductReadOnlySerializer
from Handyman.permissions import IsVendorOrVendorStaff, IsVendor, IsAdminUser

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect


class ProductViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductReadOnlySerializer
        return ProductSerializer

    # def get_permissions(self):
    #     if self.action == 'create':
    #         return [permissions.IsAuthenticated(), IsVendorOrVendorStaff]
    #     elif self.action in ['update', 'destroy']:
    #         return [IsAdminUser(), IsVendor()]
    #     elif self.action in ['list', 'retrieve']:
    #         return [permissions.IsAuthenticated(), IsVendorOrVendorStaff]
    #     return super().get_permissions()

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            queryset = self.queryset.all()
        elif user.is_authenticated:
            try:
                vendor = Vendor.objects.get(owner=user)
                queryset = self.queryset.filter(owner=vendor)
            except Vendor.DoesNotExist:
                vendor_staff = Vendor.objects.filter(staff=user)
                if vendor_staff.exists():
                    queryset = self.queryset.filter(owner__in=vendor_staff)
                else:
                    return Response({'detail': 'User is not associated with any vendor'}, status=403)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

        serializer = ProductReadOnlySerializer(queryset, many=True)
        return Response(serializer.data)

    def get_login_url(self):
        # Store the current URL in the session before redirecting to the login page
        self.request.session['next'] = self.request.get_full_path()
        return reverse('login')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_login_url()) # Redirect to login page
        else:
            return super().handle_no_permission()
