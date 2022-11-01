from reviews.models import Category, Genre, Title
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    query = Title.objects.all()
    serializer = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'category__slug', 'genre__slug')


class CategoryViewSet(viewsets.ModelViewSet):
    query = Category.objects.all()
    serializer = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'del']


class GenreViewSet(viewsets.ModelViewSet):
    query = Genre.objects.all()
    serializer = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'del']
