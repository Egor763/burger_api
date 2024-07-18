from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.core.cache import cache

from django.conf import settings

from .models import User
from .serializer import UserSerializer
from .tokens.auth import SafeJWTAuthentication
from .tokens.create_tokens import generate_access_token, generate_refresh_token
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import exceptions
from django.utils import timezone

import uuid
import hashlib
import random

SALT = (
    "8b4f6b2cc1868d75ef79e5cfb8779c11b6a374bf0fce05b485581bf4e1e25b96c8c2855015de8449"
)


class ForgotPasswordView(APIView):
    def post(self, request, format=None):
        email = request.data["email"]
        # TODO обработать ошибку неверного email

        subject = "Ссылка на забытый пароль"

        psw = ""  # предварительно создаем переменную psw
        for x in range(12):
            psw = psw + random.choice(
                list("123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
            )
        cache.set(
            "code",
            {
                "code": psw,
                "email": email,
            },
        )
        content = f"Код для сброса пароля {psw}"
        send_mail(
            subject,
            content,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        return Response(
            {
                "success": True,
                "message": "Код для сброса пароля отправлен на вашу почту.",
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    def post(self, request, format=None):
        new_password = request.data["password"]
        hashed_password = make_password(password=new_password, salt=SALT)
        token = request.data["token"]
        cache_data = cache.get("code")
        email = cache_data["email"]
        code = cache_data["code"]
        print(code)
        if token == code:
            user = User.objects.get(email=email)
            serializer_user = UserSerializer(user).data
            serializer_user["password"] = hashed_password
            serializer = UserSerializer(user, data=serializer_user, partial=True)
            if serializer.is_valid():
                serializer.save()
                cache.delete("code")

                return Response(
                    {
                        "success": True,
                        "message": "Код для сброса пароля отправлен на вашу почту.",
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    {
                        "success": False,
                        "message": "Rjl yt jnghfdkty",
                    },
                    status=status.HTTP_200_OK,
                )

        else:
            return Response(
                {
                    "success": False,
                    "message": "Rjl yt jnghfdkty",
                },
                status=status.HTTP_200_OK,
            )
