from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from inventory.organization.models import Organization

UserModel = get_user_model()


class Business(models.Model):
    class Meta:
        verbose_name_plural = "Businesses"

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

    is_visible = models.BooleanField(
        default=True,
    )

    organization = models.ForeignKey(
        to=Organization,
        on_delete=models.DO_NOTHING,
    )

    owner = models.ForeignKey(
        to=UserModel,
        on_delete=models.DO_NOTHING,
        related_name="owner",
    )

    def __str__(self):
        return self.business_name
