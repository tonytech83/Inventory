from django.test import TestCase
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class FirstUserIsSuperuserTest(TestCase):
    def test_set_first_user_superuser(self):
        first_user = UserModel.objects.create_user(email="first@first.com", password="pass123")

        first_user_in_db = UserModel.objects.first()

        self.assertEqual(first_user.is_superuser, first_user_in_db.is_superuser)

    def test_second_user_is_not_superuser(self):
        UserModel.objects.create_user(email="first@first.com", password="pass123")
        UserModel.objects.create_user(email="second@second.com", password="pass123")

        first_user_in_db = UserModel.objects.first()
        second_user_in_db = UserModel.objects.get(pk=2)

        self.assertNotEqual(second_user_in_db.is_superuser, first_user_in_db.is_superuser)
