from django.contrib.auth import get_user_model, logout
from django.contrib.auth import views as auth_views
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic as views

from inventory.accounts.forms import (
    LoginUserForm,
    ProfileEditForm,
    UserRegistrationForm,
)
from inventory.accounts.models import Profile
from inventory.core.view_mixins import OwnerRequiredMixin

UserModel = get_user_model()


class LoginView(auth_views.LoginView):
    form_class = LoginUserForm
    template_name = "accounts/login-page.html"

    def get_success_url(self):
        user = self.request.user
        profile = user.profile

        if user.is_superuser and profile.is_first_login:
            profile.is_first_login = False
            profile.save(update_fields=["is_first_login"])

            return reverse_lazy("create-organization")

        if profile.is_first_login:
            profile.is_first_login = False
            profile.save(update_fields=["is_first_login"])

            return reverse_lazy("edit-profile", kwargs={"pk": user.pk})

        return super().get_success_url()


def logout_user(request):
    logout(request)

    return redirect("dashboard")


class RegisterUserView(views.CreateView):
    queryset = UserModel.objects.all()
    template_name = "accounts/register-page.html"
    form_class = UserRegistrationForm

    success_url = reverse_lazy("login-user")


class DetailsProfileView(views.DetailView):
    # model = AppProfile
    template_name = "accounts/profile-details.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, account=self.request.user)


class EditProfileView(OwnerRequiredMixin, views.UpdateView):
    queryset = Profile.objects.all().prefetch_related("account")

    form_class = ProfileEditForm
    template_name = "accounts/edit-profile.html"

    success_url = reverse_lazy("details-profile")


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = "accounts/password_change_form.html"
    success_url = reverse_lazy("password_change_done")


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = "accounts/password_change_done.html"
