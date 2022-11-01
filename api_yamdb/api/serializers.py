from rest_framework import serializers
from api_yamdb.reviews.models import Genre
from datetime import datetime as dt

from reviews.models import Category, Title


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category')

    def validate(self, data):
        if data['year'] < dt.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!')
        return data


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')
