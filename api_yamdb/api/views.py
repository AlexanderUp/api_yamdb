from django.shortcuts import render

from reviews.models import Category, Genre, Title
from rest_framework import viewsets

#from .permissions import 
#from .serializers import CategorySerializer, GenreSerializer, TitleSerializer

class TitleViewSet(viewsets.ModelViewSet):
    # query = Title.objects.all()
    # serializer = TitleSerializer
    pass

class CategoryViewSet(viewsets.ModelViewSet):
    # query = Category.objects.all()
    # serializer = CategorySerializer
    pass

class GenreViewSet(viewsets.ModelViewSet):
    # query = Genre.objects.all()
    # serializer = GenreSerializer
    pass



