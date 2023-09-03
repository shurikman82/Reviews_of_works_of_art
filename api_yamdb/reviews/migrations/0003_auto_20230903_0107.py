# Generated by Django 3.2 on 2023-09-02 22:07

import datetime
import django.contrib.auth.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230903_0054'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='myuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.RemoveConstraint(
            model_name='myuser',
            name='username_is_not_me',
        ),
        migrations.AddField(
            model_name='myuser',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=128, verbose_name='confirmation_code'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='bio',
            field=models.TextField(default=datetime.datetime(2023, 9, 2, 22, 7, 26, 25713, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='role',
            field=models.CharField(choices=[('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='user', error_messages={'validators': 'Выбрана несуществующая роль'}, max_length=9),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(default=datetime.datetime(2023, 9, 2, 22, 7, 31, 93276, tzinfo=utc), error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
            preserve_default=False,
        ),
    ]
