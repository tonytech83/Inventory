from django.contrib.auth import views as auth_views
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views

from inventory.accounts.forms import UserRegistrationForm, LoginUserForm
from inventory.accounts.models import AppUser, AppProfile


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'
    form_class = LoginUserForm


class LogoutView(auth_views.LogoutView):
    pass


class RegisterUser(views.CreateView):
    queryset = AppUser.objects.all()
    template_name = 'accounts/register-page.html'
    form_class = UserRegistrationForm

    success_url = reverse_lazy('login-user')


class DetailsProfile(views.DetailView):
    # model = AppProfile
    template_name = 'accounts/profile-details.html'

    def get_object(self, queryset=None):
        return get_object_or_404(AppProfile, account=self.request.user)
