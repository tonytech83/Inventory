from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _

from inventory.accounts.managers import InventoryUserManager
from inventory.accounts.validators import check_name_symbols_for_non_alphabetical
from inventory.core.model_validators import phone_validator


class InventoryUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        help_text=_(
            "Provide a valid email address."
        ),
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )

    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = 'email'

    objects = InventoryUserManager()


class Profile(models.Model):
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
        upload_to='profile_pic/',
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

    is_first_login = models.BooleanField(default=True)

    account = models.OneToOneField(
        to=InventoryUser,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
    )

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'

        return 'Unknown'

    @property
    def initials(self):
        if self.first_name and self.last_name:
            return f'{self.first_name[0]}{self.last_name[0]}'.upper()

        return self.account.email[0].upper()
