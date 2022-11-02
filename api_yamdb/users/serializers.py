from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import User


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ("email", "username")
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("email", "username"),
                message="Credentials rejected"
            )
        ]

    def validate_username(self, value):
        if value == "me" or User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Prohibited username.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Prohibited email.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  # type:ignore
