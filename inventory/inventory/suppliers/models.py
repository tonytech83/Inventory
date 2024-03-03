from django.core.validators import MinLengthValidator
from django.db import models


class Supplier(models.Model):
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 50

    MIN_CONTACT_LENGTH = 6
    MAX_CONTACT_LENGTH = 50

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
        ),
        unique=True,
        null=False,
        blank=False,
    )

    contact_name = models.CharField(
        max_length=MAX_CONTACT_LENGTH,
        validators=(
            MinLengthValidator(MIN_CONTACT_LENGTH),
        ),
        null=False,
        blank=False,
    )

    phone_number = models.CharField(
        # TODO: Check how to implement this!!!
        max_length=15,
    )

    email = models.EmailField(
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name
