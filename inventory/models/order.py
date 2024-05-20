import uuid
# from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram.telegram import send_message

from inventory.models.product import Product
from inventory.models.vendor_staff import VendorStaff


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


# @receiver(post_save, sender=Order)
# def create_order_telegram_notification(sender, instance, created, **kwargs):
#     if created:
#         # Fetching all vendor staff associated with the vendor owner of the order
#         vendor_staff_list = VendorStaff.objects.filter(owner=instance.owner)
#         for vendor_staff in vendor_staff_list:
#             chat_id = vendor_staff.telegram_chat_id
#             text = f"New order {instance.display_number} has been created. \nPlease proceed to a packing area."
#             send_message(chat_id, text)
#
#
# @receiver(post_save, sender=Order)
# def update_order_telegram_notification(sender, instance, created, **kwargs):
#     if not created:
#         # Fetching all vendor staff associated with the vendor owner of the order
#         vendor_staff_list = VendorStaff.objects.filter(owner=instance.owner)
#         for vendor_staff in vendor_staff_list:
#             chat_id = vendor_staff.telegram_chat_id
#             text = f"Order {instance.display_number} has been updated.\nPlease review the changes."
#             send_message(chat_id, text)
