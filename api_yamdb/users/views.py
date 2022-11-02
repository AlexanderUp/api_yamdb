from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserCreationSerializer, UserSignupSerializer
from .utils import send_confirmation_code

User = get_user_model()


class UserCreationApiView(CreateAPIView):
    """
    User creation by admin with no confirmation code sended.
    """
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    permission_classes = (permissions.AllowAny,)
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
