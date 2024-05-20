from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from inventory.models import Vendor, VendorStaff, Product, Driver, Invoice, Supplier
from rest_framework.authtoken.models import Token
from inventory.serializers.invoice import InvoiceSerializer, InvoiceReadOnlySerializer


class VendorViewSetTestCase(TestCase):
    def setUp(self):
        # Create users
        self.superuser = User.objects.create_superuser(username='superuser', password='password')
        self.vendor_owner = User.objects.create_user(username='vendor_owner', password='password')
        self.staff_user = User.objects.create_user(username='staff_user', password='password')
        self.regular_user = User.objects.create_user(username='regular_user', password='password')

        # Create vendors
        self.vendor1 = Vendor.objects.create(
            title='Vendor 1',
            owner=self.vendor_owner
        )

        # Create VendorStaff
        self.vendor_staff = VendorStaff.objects.create(
            user=self.staff_user,
            contact_person='Staff Member',
            owner=self.vendor1
        )
        self.vendor1.staff.add(self.vendor_staff)

        self.vendor2 = Vendor.objects.create(
            title='Vendor 2',
            owner=self.vendor_owner
        )

        # Create API clients
        self.client = APIClient()
        self.superuser_token = Token.objects.create(user=self.superuser)
        self.vendor_owner_token = Token.objects.create(user=self.vendor_owner)
        self.staff_user_token = Token.objects.create(user=self.staff_user)
        self.regular_user_token = Token.objects.create(user=self.regular_user)

    def test_list_vendors_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_vendors_as_vendor_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.vendor_owner_token.key)
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_vendor_as_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
        response = self.client.get(f'/api/vendors/{self.vendor1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.vendor1.title)

    def test_retrieve_vendor_as_vendor_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.vendor_owner_token.key)
        response = self.client.get(f'/api/vendors/{self.vendor1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.vendor1.title)

    def test_retrieve_vendor_as_staff_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_user_token.key)
        response = self.client.get(f'/api/vendors/{self.vendor1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_vendor_without_authentication(self):
        response = self.client.get(f'/api/vendors/{self.vendor1.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


# class ProductViewSetTestCase(TestCase):
#     def setUp(self):
#         # Create users
#         self.superuser = User.objects.create_superuser(username='superuser', password='password')
#         self.vendor_owner = User.objects.create_user(username='vendor_owner', password='password')
#         self.staff_user = User.objects.create_user(username='staff_user', password='password')
#         self.regular_user = User.objects.create_user(username='regular_user', password='password')
#
#         # Create vendors
#         self.vendor1 = Vendor.objects.create(
#             title='Vendor 1',
#             owner=self.vendor_owner
#         )
#
#         # Create products
#         self.product1 = Product.objects.create(
#             title='Product 1',
#             price=100,
#             owner=self.vendor1
#         )
#
#         # Create VendorStaff
#         self.vendor_staff = VendorStaff.objects.create(
#             user=self.staff_user,
#             contact_person='Staff Member',
#             owner=self.vendor1
#         )
#         self.vendor1.staff.add(self.vendor_staff)
#
#         # Create API clients
#         self.client = APIClient()
#         self.superuser_token = Token.objects.create(user=self.superuser)
#         self.vendor_owner_token = Token.objects.create(user=self.vendor_owner)
#         self.staff_user_token = Token.objects.create(user=self.staff_user)
#         self.regular_user_token = Token.objects.create(user=self.regular_user)
#
#     def test_list_products_as_superuser(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
#         response = self.client.get('/api/products/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_list_products_as_vendor_owner(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.vendor_owner_token.key)
#         response = self.client.get('/api/products/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_list_products_as_staff_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_user_token.key)
#         response = self.client.get('/api/products/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_list_products_as_regular_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.regular_user_token.key)
#         response = self.client.get('/api/products/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_retrieve_product_as_superuser(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
#         response = self.client.get(f'/api/products/{self.product1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], self.product1.title)
#
#     def test_retrieve_product_as_vendor_owner(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.vendor_owner_token.key)
#         response = self.client.get(f'/api/products/{self.product1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], self.product1.title)
#
#     def test_retrieve_product_as_staff_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_user_token.key)
#         response = self.client.get(f'/api/products/{self.product1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], self.product1.title)
#
#     def test_retrieve_product_as_regular_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.regular_user_token.key)
#         response = self.client.get(f'/api/products/{self.product1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['title'], self.product1.title)


# class DriverViewSetTestCase(TestCase):
#     def setUp(self):
#         # Create users
#         self.superuser = User.objects.create_superuser(username='superuser', password='password')
#         self.vendor_owner = User.objects.create_user(username='vendor_owner', password='password')
#         self.staff_user = User.objects.create_user(username='staff_user', password='password')
#         self.regular_user = User.objects.create_user(username='regular_user', password='password')
#
#         # Create vendors
#         self.vendor1 = Vendor.objects.create(
#             title='Vendor 1',
#             owner=self.vendor_owner
#         )
#
#         # Create VendorStaff
#         self.vendor_staff = VendorStaff.objects.create(
#             user=self.staff_user,
#             contact_person='Staff Member',
#             owner=self.vendor1
#         )
#         self.vendor1.staff.add(self.vendor_staff)
#
#         self.vendor2 = Vendor.objects.create(
#             title='Vendor 2',
#             owner=self.vendor_owner
#         )
#
#         # Create drivers
#         self.driver1 = Driver.objects.create(
#             contact_person='Driver 1',
#             owner=self.vendor1
#         )
#
#         # Create API clients
#         self.client = APIClient()
#         self.superuser_token = Token.objects.create(user=self.superuser)
#         self.vendor_owner_token = Token.objects.create(user=self.vendor_owner)
#         self.staff_user_token = Token.objects.create(user=self.staff_user)
#         self.regular_user_token = Token.objects.create(user=self.regular_user)
#
#     def test_list_drivers_as_superuser(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
#         response = self.client.get('/api/drivers/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_list_drivers_as_vendor_owner(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.vendor_owner_token.key)
#         response = self.client.get('/api/drivers/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_list_drivers_as_staff_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_user_token.key)
#         response = self.client.get('/api/drivers/')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_list_drivers_without_authentication(self):
#         response = self.client.get('/api/drivers/')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_retrieve_driver_as_superuser(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser_token.key)
#         response = self.client.get(f'/api/drivers/{self.driver1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['contact_person'], self.driver1.contact_person)
#
#     def test_retrieve_driver_as_vendor_owner(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.vendor_owner_token.key)
#         response = self.client.get(f'/api/drivers/{self.driver1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['contact_person'], self.driver1.contact_person)
#
#     def test_retrieve_driver_as_staff_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_user_token.key)
#         response = self.client.get(f'/api/drivers/{self.driver1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_retrieve_driver_without_authentication(self):
#         response = self.client.get(f'/api/drivers/{self.driver1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# class InvoiceViewSetTestCase(APITestCase):
#     def setUp(self):
#         # Create users
#         self.superuser = User.objects.create_superuser(username='superuser', password='password')
#         self.vendor_owner = User.objects.create_user(username='vendor_owner', password='password')
#         self.staff_user = User.objects.create_user(username='staff_user', password='password')
#         self.regular_user = User.objects.create_user(username='regular_user', password='password')
#
#         # Create vendors
#         self.vendor1 = Vendor.objects.create(title='Vendor 1', owner=self.vendor_owner)
#         self.vendor2 = Vendor.objects.create(title='Vendor 2', owner=self.vendor_owner)
#
#         # Create suppliers
#         self.supplier1 = Supplier.objects.create(title='Supplier 1', owner=self.vendor_owner)
#         self.supplier2 = Supplier.objects.create(title='Supplier 2', owner=self.vendor_owner)
#
#         # Create VendorStaff
#         self.vendor_staff = VendorStaff.objects.create(user=self.staff_user, contact_person='Staff Member', owner=self.vendor1)
#         self.vendor1.staff.add(self.vendor_staff)
#
#         # Create invoices
#         self.invoice1 = Invoice.objects.create(owner=self.vendor1, supplier=self.supplier1)
#         self.invoice2 = Invoice.objects.create(owner=self.vendor1, supplier=self.supplier2)
#
#         # Create API clients
#         self.client = APIClient()
#         self.superuser_token = self.get_token(self.superuser)
#         self.vendor_owner_token = self.get_token(self.vendor_owner)
#         self.staff_user_token = self.get_token(self.staff_user)
#         self.regular_user_token = self.get_token(self.regular_user)
#
#     def get_token(self, user):
#         response = self.client.post('/api/token/', {'username': user.username, 'password': 'password'})
#         return response.data['access']
#
#     def test_list_invoices_as_superuser(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.superuser_token)
#         response = self.client.get('/api/invoices/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
#
#     def test_list_invoices_as_vendor_owner(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.vendor_owner_token)
#         response = self.client.get('/api/invoices/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
#
#     def test_list_invoices_as_staff_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.staff_user_token)
#         response = self.client.get('/api/invoices/')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_list_invoices_without_authentication(self):
#         response = self.client.get('/api/invoices/')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_retrieve_invoice_as_superuser(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.superuser_token)
#         response = self.client.get(f'/api/invoices/{self.invoice1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['id'], self.invoice1.id)
#
#     def test_retrieve_invoice_as_vendor_owner(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.vendor_owner_token)
#         response = self.client.get(f'/api/invoices/{self.invoice1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['id'], self.invoice1.id)
#
#     def test_retrieve_invoice_as_staff_user(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.staff_user_token)
#         response = self.client.get(f'/api/invoices/{self.invoice1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_retrieve_invoice_without_authentication(self):
#         response = self.client.get(f'/api/invoices/{self.invoice1.id}/')
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
