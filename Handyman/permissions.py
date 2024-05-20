from rest_framework import permissions
from inventory.models.vendor import Vendor
from inventory.models.vendor_staff import VendorStaff


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsVendorOrVendorStaff(permissions.BasePermission):
    # Only the vendor or vendor staff can create and update vendor inventory.
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user is associated with any vendor staff
        try:
            VendorStaff.objects.get(user=request.user)
            return True
        except VendorStaff.DoesNotExist:
            pass

        # Check if the user is associated with any vendor
        try:
            Vendor.objects.get(owner=request.user)
            return True
        except Vendor.DoesNotExist:
            return False


class IsVendor(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Check if the user is associated with any vendor
        try:
            Vendor.objects.get(owner=request.user)
            return True
        except Vendor.DoesNotExist:
            return False


class IsVendorOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # Check if the user is an administrator
        if request.user.is_staff:
            return True

        # Check if the user is associated with any vendor
        if Vendor.objects.filter(owner=request.user).exists():
            return True

        return False
