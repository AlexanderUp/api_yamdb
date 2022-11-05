# Generated by Django 2.2.16 on 2022-11-05 12:24

import django.contrib.auth.validators
from django.db import migrations, models
import users.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20221104_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator(), users.validators.me_username_validator], verbose_name='username'),
        ),
    ]