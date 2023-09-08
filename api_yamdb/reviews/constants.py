from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoleChoices(models.TextChoices):
    USER = 'user', _('Пользователь')
    ADMIN = 'admin', _('Администратор')
    MODERATOR = 'moderator', _('Модератор')
