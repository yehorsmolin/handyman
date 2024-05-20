# from django.contrib.auth.models import User
# from decimal import Decimal
# from django.test import TestCase
# from rest_framework import e2e
# from inventory.models.product import Product
# from inventory.models.category import Category
# from inventory.models.grade import Grade
# from inventory.models.color import Color
# from inventory.models.storage import Storage
# from inventory.models.status import Status
# from inventory.models.supplier import Supplier
# from inventory.models.invoice import Invoice
# from inventory.models.vendor import Vendor
# from inventory.e2e.product import ProductSerializer
# from inventory.e2e.category import CategorySerializer
# from inventory.e2e.grade import GradeSerializer
# from inventory.e2e.storage import StorageSerializer
# from inventory.e2e.color import ColorSerializer
# from inventory.e2e.status import StatusSerializer
# from inventory.e2e.supplier import SupplierSerializer
# from inventory.e2e.invoice import InvoiceSerializer
# from inventory.e2e.vendor import VendorSerializer
#
#
# class TestProductSerializer(TestCase):
#     def setUp(self):
#         self.category = Category.objects.create(title="Category 1")
#         self.storage = Storage.objects.create(title="Storage 1")
#         self.grade = Grade.objects.create(title="Grade 1")
#         self.color = Color.objects.create(title="Color 1")
#         self.status = Status.objects.create(title="Status 1")
#         self.supplier = Supplier.objects.create(title="Supplier 1")
#         self.invoice = Invoice.objects.create(invoice_number="INV12345", supplier=self.supplier)
#         self.user = User.objects.create_user(username='vendor_owner', password='password123')
#         self.vendor = Vendor.objects.create(title="Vendor Arthur", owner=self.user)
#
#         self.valid_data = {
#             'title': 'Product 1',
#             'category': self.category,  # Passing category ID instead of instance
#             'storage': self.storage,  # Passing storage ID instead of instance
#             'grade': self.grade,  # Passing grade ID instead of instance
#             'color': self.color,  # Passing color ID instead of instance
#             'price': 10.00,
#             'status': self.status,  # Passing status ID instead of instance
#             'supplier': self.supplier,  # Passing supplier ID instead of instance
#             'invoice': self.invoice,  # Passing invoice ID instead of instance
#             'owner': self.vendor,  # Passing vendor ID instead of instance
#         }
#
#     def test_serialize_instance(self):
#         serializer = ProductSerializer(data=self.valid_data)
#         self.assertTrue(serializer.is_valid())
#
#     def test_valid_serializer_data(self):
#         product = Product.objects.create(**self.valid_data)
#         serializer = ProductSerializer(instance=product)
#         self.assertEqual(serializer.data['title'], self.valid_data['title'])
#         self.assertEqual(serializer.data['category'], self.valid_data['category'].id)
#         self.assertEqual(serializer.data['storage'], self.valid_data['storage'].id)
#         self.assertEqual(serializer.data['grade'], self.valid_data['grade'].id)
#         self.assertEqual(serializer.data['color'], self.valid_data['color'].id)
#         self.assertEqual(serializer.data['price'], str(self.valid_data['price']))  # Converted to string
#         self.assertEqual(serializer.data['status'], self.valid_data['status'].id)
#         self.assertEqual(serializer.data['supplier'], self.valid_data['supplier'].id)
#         self.assertEqual(serializer.data['invoice'], self.valid_data['invoice'].uuid)
#         self.assertEqual(serializer.data['owner'], self.valid_data['owner'].id)
#
#     def test_invalid_serializer_data(self):
#         invalid_data = self.valid_data.copy()
#         invalid_data['price'] = 'invalid'  # Invalid price
#         serializer = ProductSerializer(data=invalid_data)
#         self.assertFalse(serializer.is_valid())
#         self.assertIn('price', serializer.errors)