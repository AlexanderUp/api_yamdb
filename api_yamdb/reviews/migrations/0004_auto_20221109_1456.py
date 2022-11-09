# Generated by Django 2.2.16 on 2022-11-09 14:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20221108_1634'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Category name', max_length=256, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Category slug', unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Genre name', max_length=256, verbose_name='genre'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(help_text='Genre slug', unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='review',
            name='author',
            field=models.ForeignKey(help_text="Review's author", on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, help_text='Publication date', verbose_name='pub_date'),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(help_text="Review's title score", validators=[django.core.validators.MinValueValidator(1, 'Score can not be less than one.'), django.core.validators.MaxValueValidator(10, 'Score can not be great than ten.')], verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(help_text="Review's text", verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(help_text="Title of review's subject", on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.Title', verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(help_text='Title category', on_delete=django.db.models.deletion.PROTECT, to='reviews.Category', verbose_name='category'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, help_text='Title description', null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(help_text='Title genre set', through='reviews.GenreTitle', to='reviews.Genre', verbose_name='genre'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(help_text='Title name', max_length=256, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(help_text='Title publish year', validators=[reviews.validators.validate_title_year], verbose_name='year'),
        ),
    ]
