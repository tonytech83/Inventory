from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase

from inventory.accounts.models import Profile

User = get_user_model()


class UserProfileSignalTest(TestCase):

    @patch('inventory.accounts.signals.send_successful_registration_email')
    def test_create_user_profile(self, mock_send_email):
        user = User.objects.create_user(email='test@test.com', password='pass123')
        profile_count = Profile.objects.count()
        self.assertEqual(1, profile_count)
        self.assertTrue(mock_send_email.called, "Expected 'send_successful_registration_email' to be called.")
