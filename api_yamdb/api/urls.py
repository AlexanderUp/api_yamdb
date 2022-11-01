from api.views import TitleViewSet, CategoryViewSet, GenreViewSet
from django.urls import include, path

from rest_framework.routers import DefaultRouter

app_name = "api"
router = DefaultRouter()

router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('', include(router.urls)),
]
