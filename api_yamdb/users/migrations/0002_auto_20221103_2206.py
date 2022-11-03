# Generated by Django 2.2.16 on 2022-11-03 22:06

from django.db import migrations, models
import users.utils


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('-id',), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default=users.utils.set_confirmation_code, help_text='Confirmation code', max_length=16, unique=True, verbose_name='confirmation_code'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, help_text="User's bio", max_length=2048, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with that username already exists.'}, help_text="User's email", max_length=254, unique=True, verbose_name='email'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(fields=('email', 'username'), name='email_username_uniqueness_constraint'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, username='me'), name='username_<me>_is_prohibited'),
        ),
    ]
