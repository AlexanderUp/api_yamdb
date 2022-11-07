from rest_framework import serializers

from reviews.models import Category, Genre  # isort:skip


def validate_category_slug_existance(slug):
    if not Category.objects.filter(slug=slug).exists():
        raise serializers.ValidationError(
            "Category with this slug does not exists."
        )


def validate_genre_slug_existance(slug):
    if not Genre.objects.filter(slug=slug).exists():
        raise serializers.ValidationError(
            "Genre with this slug does not exists."
        )
