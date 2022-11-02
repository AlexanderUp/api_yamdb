from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserCreationApiView, UserSignupAPIView

app_name = "users"

urlpatterns = [
    path("v1/auth/users/", UserCreationApiView.as_view(), name="create_user"),
    path("v1/auth/signup/", UserSignupAPIView.as_view(), name="signup"),
    path("v1/auth/token/", TokenObtainPairView.as_view(), name="obtain_token"),
]
