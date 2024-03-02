from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models

from inventory.accounts.managers import AccountCustomManager
from inventory.accounts.validators import phone_validator, check_name_symbols_for_non_alphabetical


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'email'

    objects = AccountCustomManager()


class AppProfile(models.Model):
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 15

    MAX_PHONE_LENGTH = 15

    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
            check_name_symbols_for_non_alphabetical,
        ),
        null=True,
        blank=True,
    )

    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
            check_name_symbols_for_non_alphabetical,
        ),
        null=True,
        blank=True,
    )

    profile_pic = models.ImageField(
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=MAX_PHONE_LENGTH,
        validators=(
            phone_validator,
        ),
        null=True,
        blank=True,
    )

    account = models.OneToOneField(
        to=AppUser,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def initials(self):
        if self.first_name and self.last_name:
            return f'{self.first_name[0]}{self.last_name[0]}'.upper()
        return self.account.email[0].upper()
