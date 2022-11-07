#!/api_yamdb/api_yamdb/api/views.py
"""All views and ViewSets."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)

from reviews.models import Category, Comment, Genre, Review, Title  # isort:skip


class NoRetrieveModelViewSet(viewsets.ModelViewSet):

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(NoRetrieveModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(NoRetrieveModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (Title.objects
                     .select_related("category")
                     .prefetch_related("genre")
                     .all())
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'category__slug', 'genre__slug', 'year')


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    base_model = Review
    id_name = "review_id"
    record_name = "review"

    def get_queryset(self):
        return self.get_base_record().comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    base_model = Title
    id_name = "title_id"
    record_name = "title"

    def get_queryset(self):
        return self.get_base_record().reviews.all()
