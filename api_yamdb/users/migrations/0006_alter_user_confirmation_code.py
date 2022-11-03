# Generated by Django 3.2.16 on 2022-11-02 18:57

import users.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20221102_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default=users.utils.set_confirmation_code, help_text='Confirmation code',
                                   max_length=16, unique=True, verbose_name='confirmation_code'),
        ),
    ]
