#!/api_yamdb/api_yamdb/api/views.py
"""All views and ViewSets."""
from django.shortcuts import render
from reviews.models import Category, Comment, Genre, Review, Title, User
from rest_framework import viewsets, mixins
from rest_framework import viewsets, filters, mixins
from .serializers import CommentSerializer, GenreSerializer, ReviewSerializer
from .serializers import UserSerializer, CategorySerializer
from .permissions import IsAdmin, ReadOnly, AuthorAdminModeratorOrReadOnly
# from .serializers import TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    pass

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


class TitleViewSet(viewsets.ModelViewSet):
    # query = Title.objects.all()
    # serializer = TitleSerializer
    pass

class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


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


class ReviewViewSet(RecordViewSet):
    serializer_class = ReviewSerializer
    base_model = Title
    id_name = "title_id"
    record_name = "title"

    def get_queryset(self):
        return self.get_base_record().reviews.all()
