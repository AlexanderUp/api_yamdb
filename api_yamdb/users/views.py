from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdmin
from .serializers import (UserSerializer, UserSignupSerializer,
                          UserTokenObtainingSerializer)
from .utils import send_confirmation_code

User = get_user_model()


class UserSignupAPIView(APIView):
    """
    Obtaining confirmation code (possibly with registration at the same time)
    by user.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():

            try:
                user, created = User.objects.get_or_create(**serializer.data)
            except IntegrityError:
                return Response(
                    serializer.data, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                if created:
                    user.set_unusable_password()  # type:ignore
                    user.save()

            send_confirmation_code(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainAPIView(APIView):
    """
    Obtaining authorization token with email and confirmation_code provided.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserTokenObtainingSerializer(data=request.data)

        if serializer.is_valid():

            username = serializer.data.get("username")
            confirmation_code = serializer.data.get("confirmation_code")

            if not User.objects.filter(username=username).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)

            if not User.objects.filter(
                confirmation_code=confirmation_code
            ).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(
                User,
                username=username,
                confirmation_code=confirmation_code
            )
            refresh_token = RefreshToken.for_user(user)
            resp = {
                "token": str(refresh_token.access_token)
            }
            return Response(
                resp, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    User viewset.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = (IsAdmin,)
    http_method_names = ["get", "post", "patch", "delete", ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user.username == instance.username:
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(instance)
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    http_method_names = ["get", "patch"]

    def get_object(self):
        obj = get_object_or_404(
            User, username=self.request.user.username  # type:ignore
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        if "role" in serializer.validated_data:
            serializer.validated_data.pop("role")
        return super().perform_update(serializer)
