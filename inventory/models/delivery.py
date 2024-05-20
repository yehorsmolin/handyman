from django.db import models

from inventory.models import Order, Driver, Vendor

from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram.telegram import send_message


class Delivery(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='delivery_orders')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, blank=True, null=True)
    pick_up_address = models.TextField(blank=True, null=True)
    delivery_address = models.CharField(max_length=200, blank=True, null=True)

    boxes = models.TextField(blank=True, null=True)
    dimensions = models.TextField(blank=True, null=True)
    weight = models.TextField(blank=True, null=True)

    owner = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    delivery_date = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Deliveries"

    def save(self, *args, **kwargs):
        # Set the pick_up_address to the shipping address of the associated vendor
        self.pick_up_address = self.owner.shipping_address
        super().save(*args, **kwargs)


# @receiver(post_save, sender=Delivery)
# def create_delivery_telegram_notification(sender, instance, created, **kwargs):
#     if created:
#         # Fetching all drivers associated with the vendor owner of the order
#         driver = instance.driver
#         chat_id = driver.telegram_chat_id
#         text = (f"New {instance.title} has been created."
#                 f"\n--------------"
#                 f"\nBoxes: {instance.boxes}"
#                 f"\nDimensions: {instance.dimensions}"
#                 f"\nWeight: {instance.weight}"
#                 f"\n--------------"
#                 f"\nPick-up address: {instance.pick_up_address}"
#                 f"\n--------------"
#                 f"\nDelivery address: {instance.delivery_address}"
#                 f"\nPlease confirm the delivery with your superviser.")
#         send_message(chat_id, text)
#
# @receiver(post_save, sender=Delivery)
# def update_delivery_telegram_notification(sender, instance, created, **kwargs):
#     if not created:
#         driver = instance.driver
#         chat_id = driver.telegram_chat_id
#         text = (f"{instance.title} has been updated."
#                 f"\n--------------"
#                 f"\nBoxes: {instance.boxes}"
#                 f"\nDimensions: {instance.dimensions}"
#                 f"\nWeight: {instance.weight}"
#                 f"\n--------------"
#                 f"\nPick-up address: {instance.pick_up_address}"
#                 f"\n--------------"
#                 f"\nDelivery address: {instance.delivery_address}"
#                 f"\nPlease confirm the delivery with your superviser.")
#         send_message(chat_id, text)
