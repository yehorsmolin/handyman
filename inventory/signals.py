from django.db.models.signals import post_delete
from django.contrib.auth.models import User

from inventory.models import Order, Vendor, Delivery, VendorStaff

from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram.telegram import send_message

from inventory.tasks import create_order_telegram_notification


@receiver(post_delete, sender=User)
def deactivate_related_vendors(sender, instance, **kwargs):
    # Get all vendors associated with the deleted user and mark them as inactive
    related_vendors = Vendor.objects.filter(owner=instance)
    related_vendors.update(is_active=False)


@receiver(post_delete, sender=User)
def deactivate_related_objects(sender, instance, **kwargs):
    # Get all vendors associated with the deleted user and mark them as inactive
    related_vendors = Vendor.objects.filter(owner=instance)
    related_vendors.update(is_active=False)

    # Get all orders associated with the deleted user and mark them as inactive
    related_orders = Order.objects.filter(user=instance)
    related_orders.update(is_active=False)

    # Mark the user as inactive instead of deleting it
    instance.is_active = False
    instance.save()


@receiver(post_save, sender=Delivery)
def create_delivery_telegram_notification(sender, instance, created, **kwargs):
    if created:
        # Fetching all drivers associated with the vendor owner of the order
        driver = instance.driver
        chat_id = driver.telegram_chat_id
        text = (f"New {instance.title} has been created."
                f"\n--------------"
                f"\nBoxes: {instance.boxes}"
                f"\nDimensions: {instance.dimensions}"
                f"\nWeight: {instance.weight}"
                f"\n--------------"
                f"\nPick-up address: {instance.pick_up_address}"
                f"\n--------------"
                f"\nDelivery address: {instance.delivery_address}"
                f"\nPlease confirm the delivery with your superviser.")
        send_message(chat_id, text)

@receiver(post_save, sender=Delivery)
def update_delivery_telegram_notification(sender, instance, created, **kwargs):
    if not created:
        driver = instance.driver
        chat_id = driver.telegram_chat_id
        text = (f"{instance.title} has been updated."
                f"\n--------------"
                f"\nBoxes: {instance.boxes}"
                f"\nDimensions: {instance.dimensions}"
                f"\nWeight: {instance.weight}"
                f"\n--------------"
                f"\nPick-up address: {instance.pick_up_address}"
                f"\n--------------"
                f"\nDelivery address: {instance.delivery_address}"
                f"\nPlease confirm the delivery with your superviser.")
        send_message(chat_id, text)


@receiver(post_save, sender=Order)
def send_create_order_telegram_notification(sender, instance: Order, created, **kwargs):
    if created:
       create_order_telegram_notification.apply_async((instance.uuid,), countdown=10)

@receiver(post_save, sender=Order)
def update_order_telegram_notification(sender, instance, created, **kwargs):
    if not created:
        # Fetching all vendor staff associated with the vendor owner of the order
        vendor_staff_list = VendorStaff.objects.filter(owner=instance.owner)
        for vendor_staff in vendor_staff_list:
            chat_id = vendor_staff.telegram_chat_id
            text = f"Order {instance.display_number} has been updated.\nPlease review the changes."
            send_message(chat_id, text)

