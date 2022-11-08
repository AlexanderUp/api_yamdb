"""All Serializers."""
from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title  # isort:skip  # noqa

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        lookup_field = "slug"
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        lookup_field = "slug"
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description",
                  "genre", "category", "rating",)

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                "Год выпуска не может быть больше текущего!"
            )
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        genre_slug_list = representation.pop("genre")
        category_slug = representation.pop("category")
        category_obj = get_object_or_404(Category, slug=category_slug)
        representation["category"] = {
            "name": category_obj.name,
            "slug": category_slug
        }
        genre_obj_list = get_list_or_404(Genre, slug__in=genre_slug_list)
        genre_representation_list = [
            {
                "name": genre.name, "slug": genre.slug
            } for genre in genre_obj_list
        ]
        representation["genre"] = genre_representation_list
        return representation

    def validate(self, validated_data):
        request = self.context.get("request")
        if request and request.method != "POST":
            return validated_data
        name = validated_data.get("name")

        if Title.objects.filter(
            name=name, category=validated_data.get("category")
        ).exists():
            raise serializers.ValidationError("Title already exists.")
        return validated_data

    def get_rating(self, object):
        queryset = object.reviews.all()
        if not queryset:
            return None
        return sum(review.score for review in queryset) / len(queryset)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
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
        fields = ("id", "author", "text", "score", "pub_date")

    def validate(self, validated_data):
        request = self.context.get("request")
        if request and request.method == "POST":
            title_id = self.context["view"].kwargs.get("title_id")
            title = get_object_or_404(Title, pk=title_id)
            if title.reviews.filter(author=request.user).exists():  # type:ignore  # noqa
                raise serializers.ValidationError(
                    "Можно оставить только один отзыв на произведение"
                )
        return validated_data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
