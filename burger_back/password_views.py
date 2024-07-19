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
        # получаем из фронтенда email
        email = request.data["email"]
        subject = "Ссылка на забытый пароль"

        psw = ""  # предварительно создаем переменную psw
        for x in range(12):
            psw = psw + random.choice(
                list("123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
            )
        # psw и email сохраняются в кэш
        cache.set(
            "code",
            {
                "code": psw,
                "email": email,
            },
        )
        content = f"Код для сброса пароля {psw}"
        # добавляются переменные для отправки кода на почту
        send_mail(
            subject,
            content,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        # возрващаем успешный ответ
        return Response(
            {
                "success": True,
                "message": "Код для сброса пароля отправлен на вашу почту.",
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    def post(self, request, format=None):
        # получаем из фронтенда пароль
        new_password = request.data["password"]
        # хэшируем пароль
        new_hashed_password = make_password(password=new_password, salt=SALT)
        # получаем из фронтенда токен
        token = request.data["token"]
        # получаем code
        cache_data = cache.get("code")
        # получаем из cache_data email
        email = cache_data["email"]
        # получаем из cache_data code
        code = cache_data["code"]
        if token == code:
            # достаем пользователя из бд по email
            user = User.objects.get(email=email)
            # переводим user из python в json
            serializer_user = UserSerializer(user).data
            # сохраняем новый пароль
            serializer_user["password"] = new_hashed_password
            # переводим user из json в python (обновляем данные пользователя)
            serializer = UserSerializer(user, data=serializer_user, partial=True)
            # если сериализатор валиден то он сохраняется
            if serializer.is_valid():
                serializer.save()
                # удаляем из кэша code
                cache.delete("code")

                return Response(
                    {
                        "success": True,
                        "message": "Код для сброса пароля отправлен на вашу почту.",
                    },
                    status=status.HTTP_200_OK,
                )

            # если сериализатор не валиден то выбрасывается ошибка
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
