from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

UserModel = get_user_model()


class TestProfile(TestCase):
    def test_first_name__with_non_alphabetical_characters__expects_validation_error(
        self,
    ):
        new_user = UserModel.objects.create_user(
            email="first@first.com", password="pass123"
        )

        new_user.profile.first_name = "1van"

        with self.assertRaises(ValidationError):
            new_user.profile.full_clean()

    def test_first_name__with_only_alphabetical_characters__expects_set(self):
        new_user = UserModel.objects.create_user(
            email="first@first.com", password="pass123"
        )

        new_user.profile.first_name = "Ivan"
        new_user.profile.full_clean()

        self.assertEqual(new_user.profile.first_name, "Ivan")

    def test_last_name__with_non_alphabetical_characters__expects_validation_error(
        self,
    ):
        new_user = UserModel.objects.create_user(
            email="first@first.com", password="pass123"
        )

        new_user.profile.last_name = "1vanov"

        with self.assertRaises(ValidationError):
            new_user.profile.full_clean()

    def test_last_name__with_only_alphabetical_characters__expects_set(self):
        new_user = UserModel.objects.create_user(
            email="first@first.com", password="pass123"
        )

        new_user.profile.first_name = "Ivanov"
        new_user.profile.full_clean()

        self.assertEqual(new_user.profile.first_name, "Ivanov")
