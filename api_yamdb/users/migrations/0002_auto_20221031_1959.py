# Generated by Django 2.2.16 on 2022-10-31 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, help_text="User's bio", max_length=2048, verbose_name='Bio'),
        ),
    ]
