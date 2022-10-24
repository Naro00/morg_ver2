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


class UserSignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "password",
            "name",
            "username",
            "email",
        )

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return user


class JWTSignupSerializer(ModelSerializer):
    username = serializers.CharField(
        required=True, write_only=True, max_length=20)
    name = serializers.CharField(required=True, write_only=True, max_length=20)
    email = serializers.CharField(
        required=True, write_only=True, style={"input_type": "email"})
    password = serializers.CharField(required=True, write_only=True, style={
                                     "input_type": "password"})

    class Meta:
        model = User
        fields = (
            "password",
            "name",
            "username",
            "email",
        )

    def save(self, request):
        user = super().save()

        user.username = self.validated_data["username"]
        user.name = self.validated_data["name"]
        user.email = self.validated_data["email"]

        user.set_password(self.validated_data["password"])
        user.save()

        return user

    def validate(self, data):
        username = data.get("username", None)

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("user already exists")

        return data


class Publicserializer(ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "avatar",
            "is_host",
        )
