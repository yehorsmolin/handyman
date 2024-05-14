from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from inventory.models import Vendor
from inventory.models import Order


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
