from email import message
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from users.models import User
from . import serializers


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        serializer = serializers.JWTSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save(request)
            login(self.request, user)

            serializer = serializers.JWTSignupSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


def complete_verification(requset, key):
    try:
        user = User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except User.DoesNotExist:
        pass
    return Response(status=status.HTTP_200_OK)


class JWTSignup(APIView):

    def post(self, request):
        password = request.data.get("password")
        password2 = request.data.get("password2")
        if password != password2:
            raise ValidationError("Passwords not equal.")
        serializer = serializers.JWTSignupSerializer(data=request.data)

        if serializer.is_valid(raise_exception=False):
            user = serializer.save(request)
            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            serializer = serializers.JWTSignupSerializer(user)

            return JsonResponse({"user": serializer.data, "access": access, "refresh": refresh},
                                status=status.HTTP_200_OK,)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST,)


class PublicUser(APIView):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        new_password2 = request.data.get("new_password2")
        if not old_password or not new_password or not new_password2:
            raise ParseError
        if len(new_password) < 8:
            raise ValidationError(
                "This password is too short. It must contain at least 8 character.")
        if new_password.isdigit():
            raise ValidationError(
                "This password is entirely numeric")
        if new_password != new_password2:
            raise ValidationError("Passwords not equal.")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)

        else:
            raise ParseError


class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "Wrong password or ID"},
                            status=status.HTTP_400_BAD_REQUEST,)


class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok": "Bye!"})


class JWTLogin(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "wrong password"})


class KakaoLogIn(APIView):
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "authorization_code",
                    "client_id": "e9f6311ab57aac58e2de4e392b18b49c",
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao",
                    "code": code,
                },
            )
            print(access_token.json())
            access_token = access_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            print(user_data.json())
            user_data = user_data.json()
            email = user_data.get("kakao_account").get("email", None)
            properties = user_data.get("properties")
            try:
                user = User.objects.get(email=email)
                login(request, user)
                return Response(status=status.HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=email,
                    username=properties.get("nickname"),
                    name=properties.get("nickname"),
                    avatar=properties.get("profile_image_url"),
                    email_verified=True,
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
