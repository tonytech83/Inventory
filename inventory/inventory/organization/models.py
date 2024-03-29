from django.core.validators import MinLengthValidator
from django.db import models


class Regions(models.TextChoices):
    ASIA = 'Asia', 'Asia'
    AFRICA = 'Africa', 'Africa'
    NORTH_AMERICA = 'North America', 'North America'
    SOUTH_AMERICA = 'South America', 'South America'
    EUROPE = 'Europe', 'Europe'
    AUSTRALIA = 'Australia', 'Australia'
    GLOBAL = 'Global', 'Global'


class Organization(models.Model):
    MIN_NAME_LENGTH = 1
    MAX_NAME_LENGTH = 30

    organization_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_NAME_LENGTH),
        ),
        null=False,
        blank=False,
    )

    region = models.CharField(
        max_length=max(len(choice[0]) for choice in Regions.choices),
        choices=Regions.choices,
        default=Regions.GLOBAL,
    )

    logo = models.ImageField(
        upload_to='organization_logo/',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.organization_name
