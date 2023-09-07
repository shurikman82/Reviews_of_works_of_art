import datetime

from django.core.exceptions import ValidationError


def title_year_validator(value):
    if value < 0 or value > datetime.datetime.now().year:
        raise ValidationError(
            f'Неверное значение года выпуска произведения: {value}!',
        )
