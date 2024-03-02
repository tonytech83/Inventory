from django.core.validators import MinLengthValidator
from django.db import models

from inventory.business.models import Business

"""

Reviewed -> may come from TimeStampedModel field `updated_at`
online -> is it possible with ping to `ip_address` (USE Redis for `In-Memory Caches`)





os -> ManyToOne to OperationSystem
sub-category -> ManyToOne to SubCategory
category -> ManyToOne to Category
manufacturer -> ManyToOne to Manufacturer
model -> ManyToOne to Model
supplier -> ManyToOne to Supplier / on_delete=models.NO
domain -> ManyToOne to Domain
"""


class OperationSystem(models.Model):
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 30
    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
        ),
    )


class Status(models.TextChoices):
    IN_OPERATION = 'In operation', 'In operation'
    RETIRED = 'Retired', 'Retired'
    PENDING_SETUP = 'Pending Setup', 'Pending Setup'
    OFFLINE = 'Offline', 'Offline'
    NOT_DEFINED_YET = 'Not defined yet', 'Not defined yet'
    EXCEPTION = 'Exception', 'Exception'


class Device(models.Model):
    MIN_NAME_LENGTH = 2
    MAX_NAME_LENGTH = 100

    MIN_SERIAL_NUMBER_LENGTH = 2
    MAX_SERIAL_NUMBER_LENGTH = 30

    MIN_OWNER_NAME_LENGTH = 2
    MAX_OWNER_NAME_LENGTH = 50

    device_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
        ),
        unique=True,
        null=False,
        blank=False,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NOT_DEFINED_YET,
    )

    ip_address = models.GenericIPAddressField(
        unique=True,
        null=True,
        blank=True,
    )

    ip_address_sec = models.GenericIPAddressField(
        unique=True,
        null=True,
        blank=True,
    )

    # serial_number ( unique, optinal )
    serial_number = models.CharField(
        max_length=MAX_SERIAL_NUMBER_LENGTH,
        validators=(
            MinLengthValidator(MIN_SERIAL_NUMBER_LENGTH),
        ),
        unique=True,
        null=True,
        blank=True,
    )

    owner_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_OWNER_NAME_LENGTH),
        ),
        default='Unknown',
    )

    business = models.ForeignKey(
        to=Business,
        on_delete=models.DO_NOTHING,
    )
