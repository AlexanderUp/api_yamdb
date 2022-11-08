"""All Serializers."""
import sys
from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .validators import (validate_category_slug_existance,
                         validate_genre_slug_existance)

from reviews.models import Category, Comment, Genre, Review, Title  # isort:skip

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = ('name', 'slug')


class CategoryLightSerializer(CategorySerializer):

    class Meta(CategorySerializer.Meta):
        extra_kwargs = {
            'name': {
                "required": False
            },
            'slug': {
                'validators': [validate_category_slug_existance],
            }
        }

    def to_internal_value(self, data):
        data = {"slug": data}
        return super().to_internal_value(data)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = ('name', 'slug')


class GenreLightSerializer(GenreSerializer):

    class Meta(GenreSerializer.Meta):
        model = Genre
        lookup_field = 'slug'
        fields = ('name', 'slug')
        extra_kwargs = {
            'name': {
                "required": False
            },
            'slug': {
                'validators': [validate_genre_slug_existance],
            }
        }

    def to_internal_value(self, data):
        data = {"slug": data}
        return super().to_internal_value(data)

    # def to_representation(self, data):
    #     value = super().to_representation(data)
    #     return value['slug']


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreLightSerializer(many=True)
    category = CategoryLightSerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value

    def validate(self, validated_data):
        request = self.context.get("request")
        if request and request.method != 'POST':
            return validated_data
        name = validated_data.get("name")
        category = validated_data.get("category")
        category_slug = category.get("slug")

        if Title.objects.filter(name=name, category__slug=category_slug).exists():
            raise serializers.ValidationError("Title already exists.")
        return validated_data

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        category_slug = category_data.get("slug")
        category = Category.objects.get(slug=category_slug)
        print("********** category", category.slug, file=sys.stderr)

        genre_data = validated_data.pop("genre")
        genre_slug_list = [genre.get("slug") for genre in genre_data]
        genre_list = Genre.objects.filter(slug__in=genre_slug_list)
        print("********** genre_list", genre_list, file=sys.stderr)

        validated_data["category"] = category
        title = Title.objects.create(**validated_data,)
        title.genre.set(genre_list)
        print("********** title", title, file=sys.stderr)
        print("********** title.genre", title.genre.all(), file=sys.stderr)
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.year = validated_data.get("year", instance.year)
        instance.description = validated_data.get(
            "description", instance.description)

        genre_slug_list = [genre.get("slug")
                           for genre in validated_data.get("genre")]
        genres = Genre.objects.filter(slug__in=genre_slug_list)
        instance.genre.set(genres)

        category = validated_data.get("category")
        category_slug = category.get("slug")
        category = Category.objects.get(slug=category_slug)
        instance.category = category
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
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

    def validate(self, validated_data):
        request = self.context.get("request")
        if request and request.method == 'POST':
            title_id = self.context['view'].kwargs.get('title_id')
            title = get_object_or_404(Title, pk=title_id)
            user = self.context['request'].user
            if Review.objects.filter(title=title, author=user).exists():
                raise serializers.ValidationError(
                    'Можно оставить только один отзыв на произведение'
                )
        return validated_data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

    # def validate(self, validated_data):
    #     request = self.context.get("request")
    #     if request and request.method == 'POST':
    #         title_id = self.context['view'].kwargs.get('title_id')
    #         title = get_object_or_404(Title, pk=title_id)
    #         user = self.context['request'].user
    #         if Review.objects.filter(title=title, author=user).exists():
    #             raise serializers.ValidationError(
    #                 'Можно оставить только один отзыв на произведение'
    #             )
    #     return validated_data
