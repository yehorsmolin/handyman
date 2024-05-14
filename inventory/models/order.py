import uuid
# from django.contrib.auth.models import User
from django.db import models

from inventory.models import Product


class Order(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        editable=False,
        default=uuid.uuid4)
    # on_delete=models.CASCADE means that if the user is deleted, all of their orders will be deleted
    # on_delete=models.SET_NULL means that if the user is deleted, the order will still exist, but the user will be set to NULL
    # on_delete=models.PROTECT means that if the user is deleted, the order will still exist, but the user will be set to NULL
    # on_delete=models.SET_DEFAULT means that if the user is deleted, the
    # order will still exist, but the user will be set to the default user

    owner = models.ForeignKey('Vendor', on_delete=models.SET_NULL, null=True)
    order_products = models.ManyToManyField(Product, related_name='orders')

    display_number = models.IntegerField(blank=False, null=False, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"Order {self.display_number}"
