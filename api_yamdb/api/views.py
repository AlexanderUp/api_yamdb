#!/api_yamdb/api_yamdb/api/views.py
"""All views and ViewSets."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters
from rest_framework.pagination import LimitOffsetPagination

from .permissions import IsAdmin, ReadOnly, IsAdminOrReadOnly
from .serializers import (CommentSerializer, GenreSerializer,
                          ReviewSerializer, CategorySerializer,
                          TitleSerializer)
from reviews.models import Category, Comment, Genre, Review, Title


class RecordViewSet(viewsets.ModelViewSet):
    pass


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    permission_classes = [IsAdmin | ReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CommentViewSet(RecordViewSet):
    serializer_class = CommentSerializer
    base_model = Review
    id_name = "review_id"
    record_name = "review"

    def get_queryset(self):
        return self.get_base_record().comments.all()


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    query = Title.objects.all()
    serializer = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'category__slug', 'genre__slug', 'year')


# class CategoryViewSet(CreateListDestroyViewSet):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    query = Category.objects.all()
    serializer = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'del']


class ReviewViewSet(RecordViewSet):
    serializer_class = ReviewSerializer
    base_model = Title
    id_name = "title_id"
    record_name = "title"

    def get_queryset(self):
        return self.get_base_record().reviews.all()
