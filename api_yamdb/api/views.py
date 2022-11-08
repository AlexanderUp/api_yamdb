"""All views and ViewSets."""
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .filters import GenreFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer)

from reviews.models import Category, Genre, Review, Title  # isort:skip
from users.permissions import CanPostAndEdit, IsAdminOrReadOnly  # isort:skip


class NoRetrieveModelViewSet(viewsets.ModelViewSet):

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
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GenreFilter
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (CanPostAndEdit,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.select_related("title").all()  # type:ignore

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(
            author=self.request.user,
            title=title
        )

    def perform_update(self, serializer):
        serializer.validated_data.pop("author", None)
        super().perform_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CanPostAndEdit,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review_obj = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review_obj.comments.all()  # type:ignore

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(
            author=self.request.user,
            review=review
        )

    def perform_update(self, serializer):
        serializer.validated_data.pop("author", None)
        super().perform_update(serializer)
