from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import USER_ROLE_CHOICES, User


class UserBaseSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=USER_ROLE_CHOICES, required=False)

    class Meta:
        model = User
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("email", "username"),
                message="User already exists."
            )
        ]

    def validate_username(self, value):
        if value == "me" or User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists or prohibited."
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  # type:ignore


class UserSerializer(UserBaseSerializer):

    class Meta(UserBaseSerializer.Meta):
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")


class UserCreationSerializer(UserBaseSerializer):

    class Meta(UserBaseSerializer.Meta):
        fields = ("email", "username", "role",)


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Prohibited username.")
        return value


class UserTokenObtainingSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        slug_field="username",
        queryset=User.objects.all()
    )
    confirmation_code = serializers.SlugRelatedField(
        slug_field="confirmation_code",
        queryset=User.objects.all()
    )

    class Meta:
        model = User
        fields = ("username", "confirmation_code",)
