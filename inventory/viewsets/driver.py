from rest_framework import viewsets
from rest_framework.response import Response
from inventory.models.driver import Driver
from inventory.models.vendor import Vendor
from inventory.models.vendor_staff import VendorStaff
from inventory.serializers.driver import DriverSerializer

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.pagination import PageNumberPagination


class DriverPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class DriverViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    pagination_class = DriverPagination

    def get_login_url(self):
        # Store the current URL in the session before redirecting to the login page
        self.request.session['next'] = self.request.get_full_path()
        return reverse('login')

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_login_url()) # Redirect to login page
        else:
            return super().handle_no_permission()

    def list(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            queryset = self.queryset.all()
        elif user.is_authenticated:
            try:
                vendor = Vendor.objects.get(owner=user)
                queryset = self.queryset.filter(owner=vendor)
            except Vendor.DoesNotExist:
                vendor_staff = VendorStaff.objects.filter(user=user)
                if vendor_staff.exists():
                    vendor_id = vendor_staff.first().owner.id
                    queryset = self.queryset.filter(owner=vendor_id)
                else:
                    return Response({'detail': 'User is not associated with any vendor'}, status=403)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

        serializer = DriverSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if user.is_superuser:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        elif user.is_authenticated:
            try:
                vendor = Vendor.objects.get(owner=user)
                if instance.owner == vendor:
                    serializer = self.get_serializer(instance)
                    return Response(serializer.data)
            except Vendor.DoesNotExist:
                vendor_staff = VendorStaff.objects.filter(user=user)
                if vendor_staff.exists():
                    vendor_id = vendor_staff.first().owner.id
                    if instance.owner.id == vendor_id:
                        serializer = self.get_serializer(instance)
                        return Response(serializer.data)
                    else:
                        return Response({'detail': 'User is not associated with any vendor'}, status=403)
            return Response({'detail': 'You do not have permission to access this product.'}, status=403)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            # If user is superuser, allow creation with any owner
            return super().create(request, *args, **kwargs)
        elif user.is_authenticated:
            try:
                vendor = Vendor.objects.get(owner=user)
                # If user is a vendor, create the product with the vendor as the owner
                request.data['owner'] = vendor.id
                return super().create(request, *args, **kwargs)
            except Vendor.DoesNotExist:
                # If user is not a vendor, check if user is a vendor staff
                vendor_staff = VendorStaff.objects.filter(user=user)
                if vendor_staff.exists():
                    # If user is a vendor staff, create the product with the associated vendor as the owner
                    vendor_id = vendor_staff.first().owner.id
                    request.data['owner'] = vendor_id
                    return super().create(request, *args, **kwargs)
                else:
                    return Response({'detail': 'User is not associated with any vendor'}, status=403)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if user.is_superuser:
            # If user is superuser, allow update
            return super().update(request, *args, **kwargs)
        elif user.is_authenticated:
            try:
                vendor = Vendor.objects.get(owner=user)
                # If user is a vendor and owns the product, allow update
                if instance.owner == vendor:
                    return super().update(request, *args, **kwargs)
                else:
                    return Response({'detail': 'You do not have permission to update this driver.'}, status=403)
            except Vendor.DoesNotExist:
                # If user is not a vendor, check if user is a vendor staff
                vendor_staff = VendorStaff.objects.filter(user=user)
                if vendor_staff.exists():
                    # If user is a vendor staff and associated with the product's vendor, allow update
                    if instance.owner == vendor_staff.first().owner:
                        return super().update(request, *args, **kwargs)
                    else:
                        return Response({'detail': 'You do not have permission to update this driver.'}, status=403)
                else:
                    return Response({'detail': 'User is not associated with any vendor'}, status=403)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        if user.is_superuser:
            # If user is superuser, allow delete
            return super().destroy(request, *args, **kwargs)
        elif user.is_authenticated:
            try:
                vendor = Vendor.objects.get(owner=user)
                # If user is a vendor and owns the product, allow delete
                if instance.owner == vendor:
                    return super().destroy(request, *args, **kwargs)
                else:
                    return Response({'detail': 'You do not have permission to delete this driver.'}, status=403)
            except Vendor.DoesNotExist:
                # If user is not a vendor, disallow delete
                return Response({'detail': 'You do not have permission to delete this product.'}, status=403)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=403)
