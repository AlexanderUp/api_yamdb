# Generated by Django 2.2.16 on 2022-10-31 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20221031_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=256),
        ),
    ]
