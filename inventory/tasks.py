from celery import shared_task
from telegram.telegram import send_message

from inventory.models import Order, Driver, VendorStaff, Delivery, Vendor

from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram.telegram import send_message

from google_sheets.api import write_available_stock_to_sheet


@shared_task
def write_stock_to_google_sheets():
    write_available_stock_to_sheet('Sheet1', 'A1')


@shared_task
def send_delivery_notification(chat_id, text):
    # This function will be executed asynchronously by Celery
    send_message(chat_id, text)


@shared_task
def create_order_telegram_notification(order_id):
    vendor_staff_list = VendorStaff.objects.filter(owner=Order.owner)
    for vendor_staff in vendor_staff_list:
        chat_id = vendor_staff.telegram_chat_id
        text = f"New order {Order.display_number} has been created. \nPlease proceed to a packing area."
        send_message(chat_id, text)

