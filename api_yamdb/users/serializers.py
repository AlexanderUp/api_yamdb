from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import User


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ("email", "username")
        constraints = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=("email", "username"),
                message="Credentials rejected"
            )
        ]

    def validata_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Prohibited username.")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  # type:ignore
