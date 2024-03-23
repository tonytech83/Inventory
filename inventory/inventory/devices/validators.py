import mimetypes
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_no_special_characters(value):
    special_characters = "!@#$%^&*()-+=[]{}|\\:;\"'<>,.?/"
    if any(char in special_characters for char in value):
        raise ValidationError(
            _('The value "%(value)s" contains special characters which are not allowed.'),
            params={'value': value},
        )


def validate_mime_type(value):
    mime_type, _ = mimetypes.guess_type(value.name)
    allowed_mime_types = ['image/jpeg', 'image/png', 'application/pdf', 'text/plain']

    if mime_type not in allowed_mime_types:
        raise ValidationError('Unsupported file type.')
