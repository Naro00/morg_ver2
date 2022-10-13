from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class PrivateUserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
        )


class SingupUserSerializer(ModelSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = User
        exclude = (
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "first_name",
            "last_name",
            "groups",
            "user_permissions",
            "avatar",
        )

    def validate(self, value):
        password = value.get("password")
        password2 = value.get("password2")

        if password != password2:
            raise serializers.ValidationError("Passwords not equal.")
        if len(password) < 8:
            raise serializers.ValidationError(
                "This password is too short. It must contain at least 8 character.")
        if password.isdigit():
            raise serializers.ValidationError(
                "This password is entirely numeric")
        return password
