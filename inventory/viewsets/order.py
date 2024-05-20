import django_filters
from rest_framework import viewsets
from rest_framework.response import Response
from inventory.models.order import Order
from inventory.models.vendor import Vendor
from inventory.models.product import Product
from inventory.models.status import Status
from inventory.models.vendor_staff import VendorStaff
from inventory.serializers.order import OrderSerializer, OrderReadOnlySerializer
from inventory.filters import OrderFilter

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.http import HttpResponseRedirect
from rest_framework.pagination import PageNumberPagination


class OrderPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]  # Add this line
    filterset_class = OrderFilter
    pagination_class = OrderPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderReadOnlySerializer
        return OrderSerializer

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

        serializer = OrderReadOnlySerializer(queryset, many=True)
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
            return Response({'detail': 'You do not have permission to access this order.'}, status=403)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    def create(self, request, *args, **kwargs):
        user = request.user
        product_ids = request.data.get('order_products', [])
        if user.is_superuser:
            # If user is superuser, allow creation with any owner
            return super().create(request, *args, **kwargs)
        elif user.is_authenticated:
            try:
                vendor = Vendor.objects.get(owner=user)
                # If user is a vendor, create the product with the vendor as the owner
                request.data['owner'] = vendor.id
                response = super().create(request, *args, **kwargs)
                # Update the status of products to 'sold'
                self.update_product_status(product_ids, status_id=6)  # Assuming 'sold' status ID is 6
                return response
            except Vendor.DoesNotExist:
                # If user is not a vendor, check if user is a vendor staff
                vendor_staff = VendorStaff.objects.filter(user=user)
                if vendor_staff.exists():
                    # If user is a vendor staff, create the product with the associated vendor as the owner
                    vendor_id = vendor_staff.first().owner.id
                    request.data['owner'] = vendor_id
                    response = super().create(request, *args, **kwargs)
                    # Update the status of products to 'sold'
                    self.update_product_status(product_ids, status_id=6)
                    return response
                else:
                    return Response({'detail': 'User is not associated with any vendor'}, status=403)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

    def update_product_status(self, product_ids, status_id):
        try:
            products = Product.objects.filter(id__in=product_ids)
            status = Status.objects.get(id=status_id)
            for product in products:
                product.status = status
                product.save()
        except Product.DoesNotExist:
            return Response({'detail': 'One or more products do not exist.'}, status=404)
        except Status.DoesNotExist:
            return Response({'detail': 'Status does not exist.'}, status=404)

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
                    return Response({'detail': 'You do not have permission to update this order.'}, status=403)
            except Vendor.DoesNotExist:
                # If user is not a vendor, check if user is a vendor staff
                vendor_staff = VendorStaff.objects.filter(user=user)
                if vendor_staff.exists():
                    # If user is a vendor staff and associated with the product's vendor, allow update
                    if instance.owner == vendor_staff.first().owner:
                        return super().update(request, *args, **kwargs)
                    else:
                        return Response({'detail': 'You do not have permission to update this order.'}, status=403)
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
                    return Response({'detail': 'You do not have permission to delete this order.'}, status=403)
            except Vendor.DoesNotExist:
                # If user is not a vendor, disallow delete
                return Response({'detail': 'You do not have permission to delete this order.'}, status=403)
        else:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)
