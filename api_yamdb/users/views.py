from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (UserCreationSerializer, UserSerializer,
                          UserSignupSerializer, UserTokenObtainingSerializer)
from .utils import send_confirmation_code

User = get_user_model()


class UserCreationApiView(CreateAPIView):
    """
    User creation by admin with no confirmation code sended.
    """
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    # permission_classes = (permissions.AllowAny,)
    # permission_classes = (permissions.IsAdminUser,)


class UserSignupAPIView(APIView):
    """
    Obtaining confirmation code by registred user.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():

            if User.objects.filter(**serializer.data).exists():
                user = User.objects.get(**serializer.data)
            else:
                email = serializer.data.get("email")
                username = serializer.data.get("username")

                if any(
                    (
                        User.objects.filter(email=email).exists(),
                        User.objects.filter(username=username).exists()
                    )
                ):
                    return Response(
                        "Email or username already used",
                        status=status.HTTP_400_BAD_REQUEST
                    )
                user = (User.objects
                            .create_user(**serializer.data))  # type:ignore
            send_confirmation_code(user)
            return Response(
                "Confirmation code sent to email",
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainAPIView(APIView):
    """
    Obtaining authorization token with email and confirmation_code provided.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserTokenObtainingSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.data.get("username"),
                confirmation_code=serializer.data.get("confirmation_code")
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
    # permission_classes = (permissions.IsAdminUser,)
    http_method_names = ["get", "post", "patch", "delete", ]


class UserAPIView(RetrieveUpdateAPIView):
    # permission_classes
    serializer_class = UserSerializer

    def get_object(self):
        return get_object_or_404(
            User, username=self.request.user.username
        )
