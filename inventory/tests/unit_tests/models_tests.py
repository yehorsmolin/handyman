from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User

from django.test import TestCase

from inventory.models.category import Category
from inventory.models.color import Color
from inventory.models.grade import Grade
from inventory.models.invoice import Invoice
from inventory.models.product import Product
from inventory.models.status import Status
from inventory.models.storage import Storage
from inventory.models.supplier import Supplier
from inventory.models.vendor import Vendor
from inventory.models.delivery import Delivery
from inventory.models.driver import Driver
from inventory.models.order import Order
from inventory.models.vendor_staff import VendorStaff


class ProductModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title="iPhone 15")
        self.storage = Storage.objects.create(title="512GB")
        self.grade = Grade.objects.create(title="A")
        self.color = Color.objects.create(title="Red")
        self.status = Status.objects.create(title="Physical")
        self.supplier = Supplier.objects.create(title="Red Dead Electronics")
        self.invoice = Invoice.objects.create(invoice_number="INV12345", supplier=self.supplier)
        self.user = User.objects.create_user(username='vendor_owner', password='password123')
        self.vendor = Vendor.objects.create(title="Vendor Arthur", owner=self.user)

    def test_product_creation(self):
        product = Product.objects.create(
            title="Test Product",
            price=Decimal("99.99"),
            description="A test product",
            category=self.category,
            storage=self.storage,
            grade=self.grade,
            color=self.color,
            status=self.status,
            supplier=self.supplier,
            invoice=self.invoice,
            imei="123456789012345",
            owner=self.vendor
        )
        self.assertEqual(product.title, "Test Product")
        self.assertEqual(product.price, Decimal("99.99"))
        self.assertEqual(product.description, "A test product")
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.storage, self.storage)
        self.assertEqual(product.grade, self.grade)
        self.assertEqual(product.color, self.color)
        self.assertEqual(product.status, self.status)
        self.assertEqual(product.supplier, self.supplier)
        self.assertEqual(product.invoice, self.invoice)
        self.assertEqual(product.imei, "123456789012345")
        self.assertEqual(product.owner, self.vendor)

    def test_product_updating(self):
        product = Product.objects.create(
            title="Test Product",
            price=Decimal("99.99"),
            description="A test product",
            category=self.category,
            storage=self.storage,
            grade=self.grade,
            color=self.color,
            status=self.status,
            supplier=self.supplier,
            invoice=self.invoice,
            imei="123456789012345",
            owner=self.vendor
        )
        product.title = "Updated Product"
        product.price = Decimal("89.99")
        product.save()

        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.title, "Updated Product")
        self.assertEqual(updated_product.price, Decimal("89.99"))

    def test_product_deletion(self):
        product = Product.objects.create(
            title="Test Product",
            price=Decimal("99.99"),
            description="A test product",
            category=self.category,
            storage=self.storage,
            grade=self.grade,
            color=self.color,
            status=self.status,
            supplier=self.supplier,
            invoice=self.invoice,
            imei="123456789012345",
            owner=self.vendor
        )
        product_id = product.id
        product.delete()

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=product_id)


class DeliveryModelTest(TestCase):

    @patch('inventory.signals.create_order_telegram_notification.apply_async')
    @patch('inventory.signals.send_message')
    def setUp(self, mock_send_message, mock_create_order_task):
        self.user = User.objects.create_user(username='vendor_owner', password='password123')
        self.vendor = Vendor.objects.create(title="Vendor Arthur", shipping_address="123 Test St", owner=self.user)
        self.driver = Driver.objects.create(contact_person="John Doe", owner=self.vendor)
        self.order = Order.objects.create(owner=self.vendor, display_number=1)
        # Ensure the order-related tasks are mocked correctly
        mock_create_order_task.assert_called_once()
        mock_send_message.assert_not_called()

    @patch('inventory.signals.send_message')
    def test_delivery_creation(self, mock_send_message):
        delivery = Delivery.objects.create(
            title="Test Delivery",
            description="A test delivery",
            order=self.order,
            driver=self.driver,
            pick_up_address=self.vendor.shipping_address,
            delivery_address="456 Delivery Ln",
            boxes="2",
            dimensions="10x10x10",
            weight="10kg",
            owner=self.vendor,
            delivery_date="2024-05-20"
        )
        self.assertEqual(delivery.title, "Test Delivery")
        self.assertEqual(delivery.description, "A test delivery")
        self.assertEqual(delivery.order, self.order)
        self.assertEqual(delivery.driver, self.driver)
        self.assertEqual(delivery.pick_up_address, "123 Test St")
        self.assertEqual(delivery.delivery_address, "456 Delivery Ln")
        self.assertEqual(delivery.boxes, "2")
        self.assertEqual(delivery.dimensions, "10x10x10")
        self.assertEqual(delivery.weight, "10kg")
        self.assertEqual(delivery.owner, self.vendor)
        self.assertEqual(delivery.delivery_date, "2024-05-20")
        mock_send_message.assert_called_once()

    @patch('inventory.signals.send_message')
    def test_delivery_updating(self, mock_send_message):
        delivery = Delivery.objects.create(
            title="Test Delivery",
            description="A test delivery",
            order=self.order,
            driver=self.driver,
            pick_up_address="123 Test St",
            delivery_address="456 Delivery Ln",
            boxes="2",
            dimensions="10x10x10",
            weight="10kg",
            owner=self.vendor,
            delivery_date="2024-05-20"
        )
        delivery.title = "Updated Delivery"
        delivery.save()

        updated_delivery = Delivery.objects.get(id=delivery.id)
        self.assertEqual(updated_delivery.title, "Updated Delivery")
        mock_send_message.assert_called()
        mock_send_message.assert_called()

    def test_delivery_deletion(self):
        delivery = Delivery.objects.create(
            title="Test Delivery",
            description="A test delivery",
            order=self.order,
            driver=self.driver,
            pick_up_address="123 Test St",
            delivery_address="456 Delivery Ln",
            boxes="2",
            dimensions="10x10x10",
            weight="10kg",
            owner=self.vendor,
            delivery_date="2024-05-20"
        )
        delivery_id = delivery.id
        delivery.delete()

        with self.assertRaises(Delivery.DoesNotExist):
            Delivery.objects.get(id=delivery_id)


class DriverModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='vendor_owner', password='password123')
        self.vendor = Vendor.objects.create(title="Vendor Arthur", owner=self.user)

    def test_driver_creation(self):
        driver = Driver.objects.create(
            contact_person="John Doe",
            plate_number="ABC123",
            phone_number="+1234567890",
            telegram_chat_id="john_doe",
            email="john@example.com",
            description="A reliable driver",
            owner=self.vendor
        )
        self.assertEqual(driver.contact_person, "John Doe")
        self.assertEqual(driver.plate_number, "ABC123")
        self.assertEqual(driver.phone_number, "+1234567890")
        self.assertEqual(driver.telegram_chat_id, "john_doe")
        self.assertEqual(driver.email, "john@example.com")
        self.assertEqual(driver.description, "A reliable driver")
        self.assertEqual(driver.owner, self.vendor)

    def test_driver_updating(self):
        driver = Driver.objects.create(
            contact_person="John Doe",
            plate_number="ABC123",
            phone_number="+1234567890",
            telegram_chat_id="john_doe",
            email="john@example.com",
            description="A reliable driver",
            owner=self.vendor
        )
        driver.contact_person = "Jane Doe"
        driver.save()

        updated_driver = Driver.objects.get(id=driver.id)
        self.assertEqual(updated_driver.contact_person, "Jane Doe")

    def test_driver_deletion(self):
        driver = Driver.objects.create(
            contact_person="John Doe",
            plate_number="ABC123",
            phone_number="+1234567890",
            telegram_chat_id="john_doe",
            email="john@example.com",
            description="A reliable driver",
            owner=self.vendor
        )
        driver_id = driver.id
        driver.delete()

        with self.assertRaises(Driver.DoesNotExist):
            Driver.objects.get(id=driver_id)


class InvoiceModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='vendor_owner', password='password123')
        self.vendor = Vendor.objects.create(title="Vendor Arthur", owner=self.user)
        self.supplier = Supplier.objects.create(title="Supplier X", owner=self.vendor)
        self.product = Product.objects.create(title="Test Product", price=10.99, owner=self.vendor)

    def test_invoice_creation(self):
        invoice = Invoice.objects.create(
            invoice_number="INV12345",
            supplier=self.supplier,
            owner=self.vendor
        )
        invoice.products.add(self.product)
        self.assertEqual(invoice.invoice_number, "INV12345")
        self.assertEqual(invoice.supplier, self.supplier)
        self.assertEqual(invoice.owner, self.vendor)
        self.assertIn(self.product, invoice.products.all())

    def test_invoice_updating(self):
        invoice = Invoice.objects.create(
            invoice_number="INV12345",
            supplier=self.supplier,
            owner=self.vendor
        )
        invoice.invoice_number = "INV54321"
        invoice.save()

        updated_invoice = Invoice.objects.get(uuid=invoice.uuid)
        self.assertEqual(updated_invoice.invoice_number, "INV54321")

    def test_invoice_deletion(self):
        invoice = Invoice.objects.create(
            invoice_number="INV12345",
            supplier=self.supplier,
            owner=self.vendor
        )
        invoice_uuid = invoice.uuid
        invoice.delete()

        with self.assertRaises(Invoice.DoesNotExist):
            Invoice.objects.get(uuid=invoice_uuid)


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='vendor_owner', password='password123')
        self.vendor = Vendor.objects.create(title="Vendor Arthur", owner=self.user)
        self.product = Product.objects.create(title="Test Product", price=10.99, owner=self.vendor)

    @patch('inventory.signals.create_order_telegram_notification.apply_async')
    def test_order_creation(self, mock_create_order_notification):
        order = Order.objects.create(
            owner=self.vendor,
            display_number=1
        )
        order.order_products.add(self.product)

        self.assertEqual(order.owner, self.vendor)
        self.assertEqual(order.display_number, 1)
        self.assertIn(self.product, order.order_products.all())
        mock_create_order_notification.assert_called_once_with((order.uuid,), countdown=10)

    @patch('inventory.signals.create_order_telegram_notification.apply_async')
    def test_order_updating(self, mock_create_order_telegram_notification):
        order = Order.objects.create(
            owner=self.vendor,
            display_number=1
        )
        order.display_number = 2
        order.save()

        updated_order = Order.objects.get(uuid=order.uuid)
        self.assertEqual(updated_order.display_number, 2)
        mock_create_order_telegram_notification.assert_called_once()

    @patch('inventory.signals.create_order_telegram_notification.apply_async')
    def test_order_deletion(self, mock_create_order_notification):
        order = Order.objects.create(
            owner=self.vendor,
            display_number=1
        )
        order_uuid = order.uuid
        order.delete()

        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(uuid=order_uuid)
        mock_create_order_notification.assert_called_once()


class VendorStaffModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='staff_user', password='password123')
        self.vendor = Vendor.objects.create(title="Vendor Corp", owner=self.user)

    def test_vendor_staff_creation(self):
        staff = VendorStaff.objects.create(
            user=self.user,
            contact_person="John Doe",
            phone_number="1234567890",
            telegram_chat_id="123457654",
            email="john@example.com",
            description="Test staff description",
            owner=self.vendor
        )

        self.assertEqual(staff.user, self.user)
        self.assertEqual(staff.contact_person, "John Doe")
        self.assertEqual(staff.phone_number, "1234567890")
        self.assertEqual(staff.telegram_chat_id, "123457654")
        self.assertEqual(staff.email, "john@example.com")
        self.assertEqual(staff.description, "Test staff description")
        self.assertEqual(staff.owner, self.vendor)

    def test_vendor_staff_updating(self):
        staff = VendorStaff.objects.create(
            user=self.user,
            contact_person="John Doe",
            phone_number="1234567890",
            telegram_chat_id="123457654",
            email="john@example.com",
            description="Test staff description",
            owner=self.vendor
        )

        staff.contact_person = "Jane Doe"
        staff.save()

        updated_staff = VendorStaff.objects.get(id=staff.id)
        self.assertEqual(updated_staff.contact_person, "Jane Doe")

    def test_vendor_staff_deletion(self):
        staff = VendorStaff.objects.create(
            user=self.user,
            contact_person="John Doe",
            phone_number="1234567890",
            telegram_chat_id="test_chat",
            email="john@example.com",
            description="Test staff description",
            owner=self.vendor
        )

        staff_id = staff.id
        staff.delete()

        with self.assertRaises(VendorStaff.DoesNotExist):
            VendorStaff.objects.get(id=staff_id)


class StorageModelTest(TestCase):

    def test_storage_creation(self):
        storage = Storage.objects.create(
            title="512GB",
            description="more storage"
        )

        self.assertEqual(storage.title, "512GB")
        self.assertEqual(storage.description, "more storage")

    def test_storage_updating(self):
        storage = Storage.objects.create(
            title="512GB",
            description="more storage"
        )

        storage.title = "1TB"
        storage.save()

        updated_storage = Storage.objects.get(id=storage.id)
        self.assertEqual(updated_storage.title, "1TB")

    def test_storage_deletion(self):
        storage = Storage.objects.create(
            title="512GB",
            description="more storage"
        )

        storage_id = storage.id
        storage.delete()

        with self.assertRaises(Storage.DoesNotExist):
            Storage.objects.get(id=storage_id)


class CategoryModelTest(TestCase):

    def test_category_creation(self):
        category = Category.objects.create(
            title="iPhone XS",
            description="old iphone"
        )

        self.assertEqual(category.title, "iPhone XS")
        self.assertEqual(category.description, "old iphone")

    def test_category_updating(self):
        category = Category.objects.create(
            title="iPhone XS",
            description="old iphone"
        )

        category.title = "even older iPhone"
        category.save()

        updated_category = Category.objects.get(id=category.id)
        self.assertEqual(updated_category.title, "even older iPhone")

    def test_category_deletion(self):
        category = Category.objects.create(
            title="iPhone XS",
            description="old iphone"
        )

        category_id = category.id
        category.delete()

        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=category_id)


class ColorModelTest(TestCase):

    def test_color_creation(self):
        color = Color.objects.create(
            title="Red",
            description="Primary color"
        )

        self.assertEqual(color.title, "Red")
        self.assertEqual(color.description, "Primary color")

    def test_color_updating(self):
        color = Color.objects.create(
            title="Red",
            description="Primary color"
        )

        color.title = "Blue"
        color.save()

        updated_color = Color.objects.get(id=color.id)
        self.assertEqual(updated_color.title, "Blue")

    def test_color_deletion(self):
        color = Color.objects.create(
            title="Red",
            description="Primary color"
        )

        color_id = color.id
        color.delete()

        with self.assertRaises(Color.DoesNotExist):
            Color.objects.get(id=color_id)


class GradeModelTest(TestCase):

    def test_grade_creation(self):
        grade = Grade.objects.create(
            title="A",
            description="Excellent"
        )

        self.assertEqual(grade.title, "A")
        self.assertEqual(grade.description, "Excellent")

    def test_grade_updating(self):
        grade = Grade.objects.create(
            title="A",
            description="Excellent"
        )

        grade.title = "B"
        grade.save()

        updated_grade = Grade.objects.get(id=grade.id)
        self.assertEqual(updated_grade.title, "B")

    def test_grade_deletion(self):
        grade = Grade.objects.create(
            title="A",
            description="Excellent"
        )

        grade_id = grade.id
        grade.delete()

        with self.assertRaises(Grade.DoesNotExist):
            Grade.objects.get(id=grade_id)


class StatusModelTest(TestCase):

    def test_status_creation(self):
        status = Status.objects.create(
            title="Pending",
            description="Waiting for processing"
        )

        self.assertEqual(status.title, "Pending")
        self.assertEqual(status.description, "Waiting for processing")

    def test_status_updating(self):
        status = Status.objects.create(
            title="Pending",
            description="Waiting for processing"
        )

        status.title = "Processing"
        status.save()

        updated_status = Status.objects.get(id=status.id)
        self.assertEqual(updated_status.title, "Processing")

    def test_status_deletion(self):
        status = Status.objects.create(
            title="Pending",
            description="Waiting for processing"
        )

        status_id = status.id
        status.delete()

        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(id=status_id)


class SupplierModelTest(TestCase):

    def test_supplier_creation(self):
        supplier = Supplier.objects.create(
            title="Supplier ABC",
            contact_person="John Doe",
            email="john@example.com",
            phone_number="123456789",
            website="http://supplierabc.com",
            billing_address="123 Billing St",
            shipping_address="456 Shipping St"
        )

        self.assertEqual(supplier.title, "Supplier ABC")
        self.assertEqual(supplier.contact_person, "John Doe")
        self.assertEqual(supplier.email, "john@example.com")
        self.assertEqual(supplier.phone_number, "123456789")
        self.assertEqual(supplier.website, "http://supplierabc.com")
        self.assertEqual(supplier.billing_address, "123 Billing St")
        self.assertEqual(supplier.shipping_address, "456 Shipping St")

    def test_supplier_updating(self):
        supplier = Supplier.objects.create(
            title="Supplier ABC",
            contact_person="John Doe",
            email="john@example.com",
            phone_number="123456789",
            website="http://supplierabc.com",
            billing_address="123 Billing St",
            shipping_address="456 Shipping St"
        )

        supplier.title = "Supplier XYZ"
        supplier.save()

        updated_supplier = Supplier.objects.get(id=supplier.id)
        self.assertEqual(updated_supplier.title, "Supplier XYZ")

    def test_supplier_deletion(self):
        supplier = Supplier.objects.create(
            title="Supplier ABC",
            contact_person="John Doe",
            email="john@example.com",
            phone_number="123456789",
            website="http://supplierabc.com",
            billing_address="123 Billing St",
            shipping_address="456 Shipping St"
        )

        supplier_id = supplier.id
        supplier.delete()

        with self.assertRaises(Supplier.DoesNotExist):
            Supplier.objects.get(id=supplier_id)