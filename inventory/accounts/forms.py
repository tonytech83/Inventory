from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model

from inventory.accounts.models import Profile

UserModel = get_user_model()


class LoginUserForm(auth_forms.AuthenticationForm):
    class Meta:
        model = UserModel
        fields = ("email", "password")


class UserRegistrationForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email",)


class ProfileBaseForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileEditForm(ProfileBaseForm):
    class Meta:
        model = Profile
        exclude = ("account", "is_first_login")
