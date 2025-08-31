from django.db import models

from inventory.accounts.models import Profile


class Days(models.TextChoices):
    MONDAY = "Monday", "Monday"
    TUESDAY = "Tuesday", "Tuesday"
    WEDNESDAY = "Wednesday", "Wednesday"
    THURSDAY = "Thursday", "Thursday"
    FRIDAY = "Friday", "Friday"
    SATURDAY = "Saturday", "Saturday"
    SUNDAY = "Sunday", "Sunday"


class Report(models.Model):
    turn_on = models.BooleanField(
        default=True,
    )

    day_of_week = models.CharField(
        max_length=10,
        choices=Days.choices,
        default=Days.MONDAY,
    )

    profile = models.OneToOneField(
        to=Profile,
        on_delete=models.CASCADE,
    )
