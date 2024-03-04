from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User

from inventory.accounts.models import AppUser, AppProfile


class LoginUserForm(auth_forms.AuthenticationForm):
    class Meta:
        model = AppUser
        fields = ('email', 'password')


class UserRegistrationForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=15, required=False)
    last_name = forms.CharField(max_length=15, required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = AppUser
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'profile_pic')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            AppProfile.objects.create(
                account=user,
                first_name=self.cleaned_data.get('first_name', None),
                last_name=self.cleaned_data.get('last_name', None),
                phone_number=self.cleaned_data.get('phone_number', None),
                profile_pic=self.cleaned_data.get('profile_pic', None),
            )
        return user


class ProfileBaseForm(forms.ModelForm):
    class Meta:
        model = AppProfile
        fields = '__all__'


class ProfileEditForm(ProfileBaseForm):
    class Meta:
        model = AppProfile
        exclude = ('account',)
