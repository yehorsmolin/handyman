import graphene
import graphene_django

from inventory.models import Category, Color, Delivery, Driver, Grade, Invoice, Order
from inventory.models import Product, Status, Storage, Supplier, Vendor, VendorStaff


class CategoryObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description']


class ColorObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Color
        fields = ['id', 'title', 'description']


class DeliveryObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Delivery
        fields = ['id', 'title', 'description', 'order', 'driver', 'pick_up_address',
                  'delivery_address', 'boxes', 'dimensions', 'weight', 'owner',
                  'is_active', 'delivery_date']


class DriverObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Driver
        fields = ['id', 'contact_person', 'plate_number', 'phone_number', 'telegram_chat_id',
                  'email', 'description', 'owner']


class GradeObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Grade
        fields = ['id', 'title', 'description']


class InvoiceObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Invoice
        fields = ['uuid', 'invoice_number', 'supplier', 'products', 'owner',
                  'created_at', 'updated_at']


class OrderObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Order
        fields = ['uuid', 'order_products', 'display_number', 'owner',
                  'created_at', 'updated_at']


class StatusObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Status
        fields = ['id', 'title', 'description']


class StorageObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Storage
        fields = ['id', 'title', 'description']


class SupplierObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Supplier
        fields = ['id', 'title', 'contact_person', 'email', 'website', 'phone_number', 'description',
                  'billing_address', 'shipping_address']


class VendorObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Vendor
        fields = ['id', 'title', 'contact_person', 'email', 'website', 'phone_number', 'description',
                  'billing_address', 'shipping_address', 'owner', 'verified', 'is_active', 'staff']


class VendorStaffObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = VendorStaff
        fields = ['id', 'user', 'contact_person', 'phone_number', 'telegram_chat_id',
                  'email', 'description', 'owner']


class ProductObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Product
        fields = ['id', 'title', 'category', 'storage', 'grade', 'price', 'status',
                  'supplier', 'invoice', 'color', 'imei', 'owner']


class PaginatedProductObjectType(graphene.ObjectType):
    nodes = graphene.List(ProductObjectType)
    total_count = graphene.Int()

class PaginatedInvoiceObjectType(graphene.ObjectType):
    nodes = graphene.List(InvoiceObjectType)
    total_count = graphene.Int()

class PaginatedDeliveryObjectType(graphene.ObjectType):
    nodes = graphene.List(DeliveryObjectType)
    total_count = graphene.Int()

class PaginatedDriverObjectType(graphene.ObjectType):
    nodes = graphene.List(DriverObjectType)
    total_count = graphene.Int()

class PaginatedOrderObjectType(graphene.ObjectType):
    nodes = graphene.List(OrderObjectType)
    total_count = graphene.Int()

class PaginatedSupplierObjectType(graphene.ObjectType):
    nodes = graphene.List(SupplierObjectType)
    total_count = graphene.Int()

class PaginatedVendorObjectType(graphene.ObjectType):
    nodes = graphene.List(VendorObjectType)
    total_count = graphene.Int()

class PaginatedVendorStaffObjectType(graphene.ObjectType):
    nodes = graphene.List(VendorStaffObjectType)
    total_count = graphene.Int()

class PaginatedStorageObjectType(graphene.ObjectType):
    nodes = graphene.List(StorageObjectType)
    total_count = graphene.Int()

class PaginatedStatusObjectType(graphene.ObjectType):
    nodes = graphene.List(StatusObjectType)
    total_count = graphene.Int()

class PaginatedGradeObjectType(graphene.ObjectType):
    nodes = graphene.List(GradeObjectType)
    total_count = graphene.Int()

class PaginatedColorObjectType(graphene.ObjectType):
    nodes = graphene.List(ColorObjectType)
    total_count = graphene.Int()

class PaginatedCategoryObjectType(graphene.ObjectType):
    nodes = graphene.List(CategoryObjectType)
    total_count = graphene.Int()



class Query(graphene.ObjectType):
    products = graphene.Field(PaginatedProductObjectType, owner_id=graphene.Int(), offset=graphene.Int(),
                              limits=graphene.Int())
    invoices = graphene.Field(PaginatedInvoiceObjectType, owner_id=graphene.Int(), offset=graphene.Int(),
                              limits=graphene.Int())
    deliveries = graphene.Field(PaginatedDeliveryObjectType, owner_id=graphene.Int(), offset=graphene.Int(),
                                limits=graphene.Int())
    drivers = graphene.Field(PaginatedDriverObjectType, owner_id=graphene.Int(), offset=graphene.Int(),
                             limits=graphene.Int())
    orders = graphene.Field(PaginatedOrderObjectType, owner_id=graphene.Int(), offset=graphene.Int(),
                            limits=graphene.Int())
    suppliers = graphene.Field(PaginatedSupplierObjectType, offset=graphene.Int(),
                               limits=graphene.Int())
    vendors = graphene.Field(PaginatedVendorObjectType, user_id=graphene.Int(), offset=graphene.Int(),
                             limits=graphene.Int())
    vendor_staff_all = graphene.Field(PaginatedVendorStaffObjectType, owner_id=graphene.Int(), offset=graphene.Int(),
                             limits=graphene.Int())
    storages = graphene.Field(PaginatedStorageObjectType, offset=graphene.Int(), limits=graphene.Int())
    statuses = graphene.Field(PaginatedStatusObjectType, offset=graphene.Int(), limits=graphene.Int())
    grades = graphene.Field(PaginatedGradeObjectType, offset=graphene.Int(), limits=graphene.Int())
    colors = graphene.Field(PaginatedColorObjectType, offset=graphene.Int(), limits=graphene.Int())
    categories = graphene.Field(PaginatedCategoryObjectType, offset=graphene.Int(), limits=graphene.Int())

    def resolve_products(self, info, owner_id=None, offset=None, limit=None):
        # Check if vendor_id is provided
        if owner_id is None:
            return []

        total_count = Product.objects.filter(owner=owner_id).count()

        product_qs = Product.objects.filter(owner=owner_id)

        if offset is not None:
            product_qs = product_qs[offset:]
        if limit is not None:
            product_qs = product_qs[:limit]

        return {
            "nodes": product_qs,
            "total_count": total_count,
        }

    def resolve_invocies(self, info, owner_id=None, offset=None, limit=None):
        # Check if vendor_id is provided
        if owner_id is None:
            return []

        total_count = Invoice.objects.filter(owner=owner_id).count()

        invoices_qs = Invoice.objects.filter(owner=owner_id)

        if offset is not None:
            product_qs = invoices_qs[offset:]
        if limit is not None:
            product_qs = invoices_qs[:limit]

        return {
            "nodes": invoices_qs,
            "total_count": total_count,
        }


    def resolve_deliveries(self, info, owner_id=None, offset=None, limit=None):
        # Check if vendor_id is provided
        if owner_id is None:
            return []

        total_count = Delivery.objects.filter(owner=owner_id).count()

        delivery_qs = Delivery.objects.filter(owner=owner_id)

        if offset is not None:
            delivery_qs = delivery_qs[offset:]
        if limit is not None:
            delivery_qs = delivery_qs[:limit]

        return {
            "nodes": delivery_qs,
            "total_count": total_count,
        }

    def resolve_drivers(self, info, owner_id=None, offset=None, limit=None):
        # Check if vendor_id is provided
        if owner_id is None:
            return []

        total_count = Driver.objects.filter(owner=owner_id).count()

        driver_qs = Driver.objects.filter(owner=owner_id)

        if offset is not None:
            driver_qs = driver_qs[offset:]
        if limit is not None:
            driver_qs = driver_qs[:limit]

        return {
            "nodes": driver_qs,
            "total_count": total_count,
        }


    def resolve_orders(self, info, owner_id=None, offset=None, limit=None):
        # Check if vendor_id is provided
        if owner_id is None:
            return []

        total_count = Order.objects.filter(owner=owner_id).count()

        order_qs = Order.objects.filter(owner=owner_id)

        if offset is not None:
            order_qs = order_qs[offset:]
        if limit is not None:
            order_qs = order_qs[:limit]

        return {
            "nodes": order_qs,
            "total_count": total_count,
        }

    def resolve_suppliers(self, info, offset=None, limit=None):

        total_count = Supplier.objects.count()

        supplier_qs = Supplier.objects.all()

        if offset is not None:
            supplier_qs = supplier_qs[offset:]
        if limit is not None:
            supplier_qs = supplier_qs[:limit]

        return {
            "nodes": supplier_qs,
            "total_count": total_count,
        }

    def resolve_vendors(self, info, user_id=None, offset=None, limit=None):
        # Check if vendor_id is provided
        if user_id is None:
            return Vendor.objects.all()
        return Vendor.objects.filter(user_id=user_id)

    def resolve_vendor_staff_all(self, info, owner_id=None, offset=None, limit=None):
        # Check if vendor_id is provided
        if owner_id is None:
            return []

        total_count = VendorStaff.objects.filter(owner=owner_id).count()

        vendor_staff_qs = VendorStaff.objects.filter(owner=owner_id)

        if offset is not None:
            vendor_staff_qs = vendor_staff_qs[offset:]
        if limit is not None:
            vendor_staff_qs = vendor_staff_qs[:limit]

        return {
            "nodes": vendor_staff_qs,
            "total_count": total_count,
        }

    def resolve_storages(self, info, offset=None, limit=None):
        return Storage.objects.all()

    def resolve_statuses(self, info, offset=None, limit=None):
        return Status.objects.all()

    def resolve_grades(self, info, offset=None, limit=None):
        return Grade.objects.all()

    def resolve_colors(self, info, offset=None, limit=None):
        return Color.objects.all()

    def resolve_categories(self, info, offset=None, limit=None):
        return Category.objects.all()

schema = graphene.Schema(query=Query)