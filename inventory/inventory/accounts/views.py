from django.contrib.auth import views as auth_views
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views

from inventory.accounts.forms import UserRegistrationForm, LoginUserForm, ProfileEditForm
from inventory.accounts.models import AppUser, AppProfile


class LoginView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'
    form_class = LoginUserForm


class LogoutView(auth_views.LogoutView):
    pass


class RegisterUserView(views.CreateView):
    queryset = AppUser.objects.all()
    template_name = 'accounts/register-page.html'
    form_class = UserRegistrationForm

    success_url = reverse_lazy('login-user')


class DetailsProfileView(views.DetailView):
    # model = AppProfile
    template_name = 'accounts/profile-details.html'

    def get_object(self, queryset=None):
        return get_object_or_404(AppProfile, account=self.request.user)


class EditProfileView(views.UpdateView):
    queryset = (AppProfile.objects.all()
                .prefetch_related('account'))
    form_class = ProfileEditForm
    template_name = 'accounts/edit-profile.html'

    success_url = reverse_lazy('details-profile')


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('password_change_done')


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'
