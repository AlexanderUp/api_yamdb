"""All views and ViewSets."""
from django.db.models.aggregates import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .filters import GenreFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadOnlySerializer, TitleSerializer)

from reviews.models import Category, Genre, Review, Title  # isort:skip
from users.permissions import CanPostAndEdit, IsAdminOrReadOnly  # isort:skip


class NoRetrieveModelViewSet(viewsets.ModelViewSet):

    def retrieve(self, request, *args, **kwargs):
        msg_dict = {"detail": "Method \"GET\" is not allowed."}
        return Response(msg_dict, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommonViewSetMixin():
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = "slug"
    http_method_names = ['get', 'post', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(CommonViewSetMixin, NoRetrieveModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CommonViewSetMixin, NoRetrieveModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg("reviews__score")
    ).select_related(
        "category"
    ).prefetch_related(
        "genre"
    ).order_by('-id').all()

    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = GenreFilter

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadOnlySerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (CanPostAndEdit,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return (title.reviews  # type:ignore
                     .select_related("title", "author")
                     .all())

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(
            author=self.request.user,
            title=title
        )

    def perform_update(self, serializer):
        """
        Для предотвращения подмены автора отзыва на произведение
        при использовании метода PATCH удаляем из валидированных
        данных ключ 'автор'.
        """
        serializer.validated_data.pop("author", None)
        super().perform_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CanPostAndEdit,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review_obj = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return (review_obj.comments  # type:ignore
                          .select_related("author", "review")
                          .all())

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(
            author=self.request.user,
            review=review
        )

    def perform_update(self, serializer):
        """
        Для предотвращения подмены автора комментария на отзыв
        при использовании метода PATCH удаляем из валидированных
        данных ключ 'автор'.
        """
        serializer.validated_data.pop("author", None)
        super().perform_update(serializer)
