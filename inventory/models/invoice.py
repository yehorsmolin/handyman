import uuid
from django.db import models
from django.utils import timezone
from inventory.models.supplier import Supplier


class Invoice(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_number = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', related_name='product_invoices')
    owner = models.ForeignKey('Vendor', on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.invoice_number
