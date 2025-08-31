from django.core.exceptions import ValidationError


def check_name_symbols_for_non_alphabetical(value):
    if not value.isalpha():
        raise ValidationError(
            f"`{value}` must be only alphabet symbol without whitespace."
        )
