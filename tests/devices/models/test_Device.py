from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from inventory.business.models import Business
from inventory.devices.models import Device
from inventory.organization.models import Organization

UserModel = get_user_model()


class TestDevice(TestCase):

    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(email="test@test.com", password="pass123")
        self.organization = Organization.objects.create(organization_name="A")
        self.business = Business.objects.create(
            business_name='B',
            country='C',
            organization=self.organization,
            owner=self.user
        )

    def test_validate_no_special_characters__raises_validation_error(self):
        device = Device(device_name='test', serial_number='test1234', business=self.business, operating_system='@')

        with self.assertRaises(ValidationError):
            device.full_clean()

    def test_validate_po_number__with_valid_number(self):
        po_number = 1234567890

        device = Device(device_name='test', serial_number='test1234', business=self.business,
                        purchase_order_number=po_number)
        device.full_clean()

    def test_validate_po_number__with_invalid_number(self):
        po_number = 12345678901

        device = Device(device_name='test', serial_number='test1234', business=self.business,
                        purchase_order_number=po_number)

        with self.assertRaises(ValidationError):
            device.full_clean()
