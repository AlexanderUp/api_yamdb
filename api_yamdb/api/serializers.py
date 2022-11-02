#!/api_yamdb/api_yamdb/api/serializers.py
"""All Serializers."""
from datetime import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title  # isort:skip


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category')

    def validate(self, data):
        if data['year'] < dt.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitlePostSerializer(serializers.ModelSerializer):
    pass


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    score = serializers.IntegerField(
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        )
    )

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        user = self.context['request'].user
        if Review.objects.filter(title=title, author=user).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
