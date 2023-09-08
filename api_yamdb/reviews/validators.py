from django.utils import timezone

from django.core.exceptions import ValidationError


def title_year_validator(value):
    if value < 0 or value > timezone.now().year:
        raise ValidationError(
            f'Неверное значение года выпуска произведения: {value}!',
        )
