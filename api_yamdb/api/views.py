"""All views and ViewSets."""
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)

from reviews.models import Category, Comment, Genre, Review, Title  # isort:skip
from users.permissions import CanPostAndEdit, IsAdmin, IsAdminOrReadOnly  # isort:skip


class NoRetrieveModelViewSet(viewsets.ModelViewSet):

    # def update(self, request, *args, **kwargs):
    #     msg_dict = {"detail": "Method \"PUT\" not allowed."}
    #     return Response(msg_dict, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        msg_dict = {"detail": "Method \"GET\" not allowed."}
        return Response(msg_dict, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(NoRetrieveModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    http_method_names = ['get', 'post', 'delete']
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
    # permission_classes = (AllowAny,)
    # permission_classes = (IsAdminOrReadOnly,)
    permission_classes = (CanPostAndEdit,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'category__slug', 'genre__slug', 'year')
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    permission_classes = (CanPostAndEdit,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Review.objects.filter(title_id=self.kwargs.get("title_id"))

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CanPostAndEdit,)

    def get_queryset(self):
        review_obj = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review_obj.comments.all()  # type:ignore
