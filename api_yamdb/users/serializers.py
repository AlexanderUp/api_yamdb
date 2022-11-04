from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")

    def validate_username(self, value):
        if value == "me" or User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username exists or prohibited.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)  # type:ignore


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError("Prohibited username.")
        return value


class UserTokenObtainingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=16)

    class Meta:
        model = User
        fields = ("username", "confirmation_code",)
