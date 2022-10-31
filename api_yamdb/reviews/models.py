from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name
    
    @classmethod
    def get_default_pk(cls):
        obj, created = cls.objects.get_or_create(name='No category')
        return obj.pk


class Genre(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
    
    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=150)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_DEFAULT,
        default = Category.get_default_pk
        )
    genre = models.ManyToManyField(Genre)
    
    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
    
    def __str__(self):
        return self.name