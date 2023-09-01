import random

from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    bio = models.TextField()
    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=9, default='user',
        error_messages={'validators': 'Выбрана несуществующая роль'}
    )
    confirmation_code = models.CharField(
        'confirmation_code', blank=True, max_length=128)

    def make_confirmation_code(self):
        self.confirmation_code = random.randint(10000, 100000)
        return self.confirmation_code

    def check_confirmation_code(self, email_confirmation_code):
        if email_confirmation_code == self.confirmation_code:
            return True
        return False\


    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
