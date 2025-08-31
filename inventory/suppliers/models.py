from django.core.validators import MinLengthValidator
from django.db import models

from inventory.core.model_validators import phone_validator


class Supplier(models.Model):
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 50

    MIN_CONTACT_LENGTH = 6
    MAX_CONTACT_LENGTH = 50

    MIN_COUNTRY_LENGTH = 3
    MAX_COUNTRY_LENGTH = 60

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(MinLengthValidator(MIN_NAME_LENGTH),),
        unique=True,
        null=False,
        blank=False,
    )

    contact_name = models.CharField(
        max_length=MAX_CONTACT_LENGTH,
        validators=(MinLengthValidator(MIN_CONTACT_LENGTH),),
        null=False,
        blank=False,
    )

    supplier_country = models.CharField(
        max_length=MAX_COUNTRY_LENGTH,
        validators=(MinLengthValidator(MIN_COUNTRY_LENGTH),),
        null=False,
        blank=False,
    )

    phone_number = models.CharField(
        max_length=15,
        validators=(phone_validator,),
    )

    email = models.EmailField(
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name
