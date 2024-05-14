from django.db import models
from django.core.validators import MinValueValidator

from inventory.models.category import Category
from inventory.models.grade import Grade
from inventory.models.color import Color
from inventory.models.status import Status
from inventory.models.supplier import Supplier
from inventory.models.storage import Storage
from inventory.models.invoice import Invoice


class Product(models.Model):
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=7, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True)
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, blank=True, null=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, blank=True, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, blank=True, null=True)
    imei = models.CharField(max_length=120)

    owner = models.ForeignKey('Vendor', on_delete=models.SET_NULL, null=True, related_name='owners_of_product')

    # ActiveRecord
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.title} - {self.storage} - {self.grade} - {self.color} - {self.imei} - {self.price}"
