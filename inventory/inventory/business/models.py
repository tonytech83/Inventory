from django.core.validators import MinLengthValidator
from django.db import models

from inventory.accounts.models import AppUser


class Business(models.Model):
    MIN_BUSINESS_LENGTH = 2
    MAX_BUSINESS_LENGTH = 30

    MIN_COUNTRY_LENGTH = 3
    MAX_COUNTRY_LENGTH = 60

    business_name = models.CharField(
        max_length=MAX_BUSINESS_LENGTH,
        validators=(
            MinLengthValidator(MIN_BUSINESS_LENGTH),
        ),
        unique=True,
        null=False,
        blank=False,
    )

    country = models.CharField(
        max_length=MAX_COUNTRY_LENGTH,
        validators=(
            MinLengthValidator(MIN_COUNTRY_LENGTH),
        ),
        null=False,
        blank=False,
    )

    business_picture = models.ImageField(
        null=True,
        blank=True,
    )

    is_visible = models.BooleanField(
        default=True
    )

    owner = models.ForeignKey(
        to=AppUser,
        on_delete=models.DO_NOTHING,
        related_name="owner",
    )

    def __str__(self):
        return self.business_name
