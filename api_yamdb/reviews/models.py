#!/api_yamdb/api_yamdb/reviews/models.py
"""All models."""
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Категории (типы) произведений."""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    @classmethod
    def get_default_pk(cls):
        obj, created = cls.objects.get_or_create(name='No category')
        return obj.pk


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
    """
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=Category.get_default_pk
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Категории жанров."""
    name = models.CharField(max_length=256, verbose_name='Жанр')
    slug = models.SlugField(
        max_length=50, verbose_name='Идентификатор', unique=True)
    title = models.ManyToManyField(Title)

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews',
        help_text='Автор отзыва')
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Произведение',
        related_name='reviews',
        help_text='Произведение на которое написан отзыв')
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True,
        help_text='Дата публикации отзыва')
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        help_text='Введдите оценку')

    class Meta:
        ordering = ['pub_date']
        constraints = [models.UniqueConstraint(
            fields=['author', 'title'],
            name='only_one_review')]


class Comment(models.Model):
    """Комментарии к отзывам."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор комментария')
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Отзыв',
        related_name='comments',
        help_text='Отзыв, к которому написан комментарий')
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        db_index=True,
        auto_now_add=True,
        help_text='Дата публикации комментария')

    class Meta:
        ordering = ['pub_date']
