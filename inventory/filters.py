import django_filters
from inventory.models.product import Product
from inventory.models.order import Order
from inventory.models.invoice import Invoice
from inventory.models.delivery import Delivery


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    category = django_filters.CharFilter(field_name='category__title', lookup_expr='exact')
    grade = django_filters.CharFilter(field_name='grade__title', lookup_expr='exact')
    color = django_filters.CharFilter(field_name='color__title', lookup_expr='exact')
    storage = django_filters.CharFilter(field_name='storage__title', lookup_expr='exact')
    status = django_filters.CharFilter(field_name='status__title', lookup_expr='exact')
    supplier = django_filters.CharFilter(field_name='supplier__title', lookup_expr='exact')
    invoice = django_filters.CharFilter(field_name='invoice__number', lookup_expr='exact')

    class Meta:
        model = Product
        fields = {
            'title': ['icontains'], # Filtering by title
            'price': ['lt', 'gt'], # Filtering by price
            'category': ['exact'],  # Filtering by category
            'grade': ['exact'],  # Filtering by grade
            'color': ['exact'],  # Filtering by color
            'status': ['exact'],  # Filtering by status
            'storage': ['exact'],  # Filtering by storage
            'supplier': ['exact'],  # Filtering by supplier
            'invoice': ['exact'],  # Filtering by invoice
            'created_at': ['date__gt', 'date__lt'], # Filtering by creation date
        }


class OrderFilter(django_filters.FilterSet):
    created_at__gt = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lt = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Order
        fields = {
            'order_products__title': ['icontains'],  # Filtering by order product title
            'display_number': ['exact'],  # Filtering by display number
        }


class InvoiceFilter(django_filters.FilterSet):
    class Meta:
        model = Invoice
        fields = {
            'invoice_number': ['exact'],  # Filtering by invoice number
            'supplier__title': ['icontains'],  # Filtering by supplier title
            'created_at': ['date__gt', 'date__lt'],  # Filtering by creation date range
        }


class DeliveryFilter(django_filters.FilterSet):
    class Meta:
        model = Delivery
        fields = {
            'title': ['icontains'],  # Filtering by title
            'order__display_number': ['exact'],  # Filtering by order display number
            'driver__contact_person': ['icontains'],  # Filtering by driver name
            'pick_up_address': ['icontains'],  # Filtering by pick-up address
            'delivery_address': ['icontains'],  # Filtering by delivery address
            'is_active': ['exact'],  # Filtering by activity status
            'delivery_date': ['icontains'],  # Filtering by delivery date
        }