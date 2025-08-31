import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from inventory.business.models import Business
from inventory.devices.models import Device
from inventory.organization.models import Organization

UserModel = get_user_model()


class BusinessViewTests(TestCase):
    def setUp(self) -> None:
        self.user = UserModel.objects.create_user(email="test@test.com", password="pass123")
        self.organization = Organization.objects.create(organization_name="A")
        self.business = Business.objects.create(
            business_name='B',
            country='C',
            organization=self.organization,
            owner=self.user
        )

    def test_get_business__when_anonymous_user__expects_404(self):
        response = self.client.get(f'business/{self.business.pk}')

        self.assertEqual(response.status_code, 404)

    def test_get_business__when_user_is_owner__expects_200(self):
        self.client.login(email="test@test.com", password="pass123")

        response = self.client.get(reverse('business', kwargs={'pk': self.business.pk}), follow=True)

        self.assertEqual(response.status_code, 200)

    def test_get_business__when_user_is_not_owner__expects_200(self):
        new_user = UserModel.objects.create_user(email="new_test@test.com", password="pass123")
        self.client.login(email="new_test@test.com", password="pass123")

        response = self.client.get(reverse('business', kwargs={'pk': self.business.pk}), follow=True)

        self.assertEqual(response.status_code, 200)

    def test_get_business__when_user_is_owner_and_single_device(self):
        device = Device.objects.create(device_name='test', serial_number='test1234', business=self.business)

        self.client.login(email="test@test.com", password="pass123")

        self.client.get(reverse('home-page'))

        response = self.client.get(reverse('business', kwargs={'pk': self.business.pk}), follow=True)

        actual_devices_json = json.loads(response.context['devices_json'])

        actual_devices_json = [{
            'device_name': d['device_name'],
            'serial_number': d['serial_number']
        } for d in actual_devices_json]

        expected_data = [{
            'device_name': device.device_name,
            'serial_number': device.serial_number,
        }]

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(expected_data, actual_devices_json)
