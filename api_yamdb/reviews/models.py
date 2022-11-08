"""All models."""
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Категории (типы) произведений."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Категории жанров."""
    name = models.CharField(max_length=256, verbose_name="Жанр")
    slug = models.SlugField(
        max_length=50, verbose_name="Идентификатор жанра", unique=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы (определённый фильм, книга или песня).
    """
    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(Genre, through="GenreTitle")

    class Meta:
        ordering = ("-id",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        constraints = [
            models.UniqueConstraint(
                fields=("name", "category"),
                name="unique_title_name_category"
            ),
        ]

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзывы."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="reviews",
        help_text="Автор отзыва")
    text = models.TextField(
        "Текст отзыва",
        help_text="Введите текст отзыва")
    title = models.ForeignKey(
        Title,
        related_name="reviews",
        on_delete=models.CASCADE,
        verbose_name="Произведение",
        help_text="Произведение, на которое написан отзыв")
    pub_date = models.DateTimeField(
        "Дата публикации отзыва",
        auto_now_add=True,
        db_index=True,
        help_text="Дата публикации отзыва")
    score = models.IntegerField(
        "Оценка",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        help_text="Введите оценку")

    class Meta:
        ordering = ("-id",)
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name="only_one_review"
            ),
        ]


class Comment(models.Model):
    """Комментарии к отзывам."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
        help_text="Автор комментария")
    text = models.TextField(
        "Текст комментария",
        help_text="Введите текст комментария")
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="Отзыв",
        related_name="comments",
        help_text="Отзыв, к которому написан комментарий")
    pub_date = models.DateTimeField(
        "Дата публикации комментария",
        db_index=True,
        auto_now_add=True,
        help_text="Дата публикации комментария")

    class Meta:
        ordering = ("-id",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="genre_id",
        help_text="Genre ID",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="title_id",
        help_text="Title ID",
    )

    class Meta:
        ordering = ("-id",)
        verbose_name = "GenreTitle"
        verbose_name_plural = "GenreTitles"
