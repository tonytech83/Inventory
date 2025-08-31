import re

from django.core.exceptions import ValidationError


def phone_validator(value):
    match = re.match(r"^(0|\+359)(\d{9})\b", value)
    if not match:
        raise ValidationError("Valid phone format is 0xxxxxxxxx or +359xxxxxxxxxx.")
