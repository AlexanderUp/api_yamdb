# Generated by Django 2.2.16 on 2022-10-31 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.AddField(
            model_name='genre',
            name='title',
            field=models.ManyToManyField(to='reviews.Title'),
        ),
    ]
