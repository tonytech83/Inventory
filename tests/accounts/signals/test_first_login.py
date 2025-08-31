from django.test import TestCase
from django.contrib.auth import get_user_model


User = get_user_model()


# class UserLoginSignalTest(TestCase):
#     def test_first_login_signal_sets_session_flag(self):
#         user1 = User.objects.create_user(email='test1@test.com', password='pass123')
#         user2 = User.objects.create_user(email='test2@test.com', password='pass123')
#
#         self.client.login(username='test2@test.com', password='pass123')
#
#         self.assertEqual(False, user2.profile.is_first_login)
