from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

UserModel = get_user_model()


class LoginViewTests(TestCase):
    def setUp(self):
        self.superuser = UserModel.objects.create_superuser(email='superuser@test.com', password='pass123')
        self.superuser.profile.is_first_login = True
        self.superuser.profile.save()

        self.staff_user = UserModel.objects.create_user(email='user@test.com', password='pass123')
        self.staff_user.profile.is_first_login = True
        self.staff_user.profile.save()

    def test_superuser_first_login_redirects_to_create_organization(self):
        response = self.client.post(reverse('login-user'), {'username': 'superuser@test.com', 'password': 'pass123'})

        self.assertRedirects(response, reverse_lazy('create-organization'))

    def test_regular_user_first_login_redirects_to_edit_profile(self):
        response = self.client.post(reverse('login-user'), {'username': 'user@test.com', 'password': 'pass123'})

        self.assertRedirects(response, reverse_lazy('edit-profile', kwargs={'pk': self.staff_user.pk}))

    def test_subsequent_login_redirects_to_default_success_url(self):

        self.staff_user.profile.is_first_login = False
        self.staff_user.profile.save()
        response = self.client.post(reverse('login-user'), {'username': 'user@test.com', 'password': 'pass123'})

        self.assertRedirects(response, reverse('home-page'))
