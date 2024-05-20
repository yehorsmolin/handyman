from django.contrib import admin

from inventory.models import Product, Category, Color, Grade, Order, Status, Supplier, Vendor, VendorStaff
from inventory.models import Storage, Invoice, Driver, Delivery


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Grade)
admin.site.register(Vendor)
admin.site.register(VendorStaff)
admin.site.register(Status)
admin.site.register(Supplier)
admin.site.register(Order)
admin.site.register(Storage)
admin.site.register(Invoice)
admin.site.register(Driver)
admin.site.register(Delivery)

