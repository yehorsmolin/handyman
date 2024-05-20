# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from datetime import datetime
# from inventory.models import Delivery
# from inventory.models import Driver
# from rest_framework.response import Response
#
# from telegram.telegram import send_message
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
#
# def process_delivery_message(chat_id, message, vendor):
#     # Split the message into order number and action
#     order_number, action = message.split(' ')
#
#     # Find the delivery object based on the order number
#     try:
#         delivery = Delivery.objects.get(order__display_number=order_number)
#     except Delivery.DoesNotExist:
#         # Handle the case where the delivery does not exist
#         return "Delivery not found"
#
#     # Find the driver associated with the vendor owner of the order
#     try:
#         driver = Driver.objects.get(owner=vendor)
#     except Driver.DoesNotExist:
#         # Handle the case where the driver does not exist
#         return "Driver not found"
#
#     # Check if the message was sent from the correct chat ID
#     if driver.telegram_chat_id != chat_id:
#         return "Message sent from an unauthorized chat ID"
#
#     # Check if the action is 'delivered'
#     if action.lower() == 'delivered':
#         # Update the delivery object
#         delivery.is_active = False
#         delivery.delivery_date = datetime.now()
#         delivery.save()
#
#         return "Delivery status updated successfully"
#     else:
#         return "Invalid action"
#
#
# @api_view(['POST'])
# @authentication_classes([])
# @permission_classes([])
# def telegram(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         chat_id = data['message']['chat']['id']
#         message_text = data['message']['text']
#         vendor = get_vendor_for_chat_id(chat_id)  # Implement this function later
#         response_text = process_delivery_message(chat_id, message_text, vendor)
#         send_message(chat_id, response_text)
#         return JsonResponse({'status': 'ok'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'Unsupported method'}, status=405)
