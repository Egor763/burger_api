from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Card, User
from .serializer import CardSerializer, UserSerializer
from .tokens.auth import SafeJWTAuthentication
from .tokens.create_tokens import generate_access_token, generate_refresh_token
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import exceptions


SALT = (
    "8b4f6b2cc1868d75ef79e5cfb8779c11b6a374bf0fce05b485581bf4e1e25b96c8c2855015de8449"
)


class RegistrationView(APIView):
    def post(self, request, format=None):
        # хэширование пароля
        request.data["password"] = make_password(
            password=request.data["password"], salt=SALT
        )

        # del serializer_user["password"]
        # генерируем access_token
        access_token = generate_access_token(request.data)
        # генерируем refresh_token
        refresh_token = generate_refresh_token(request.data)
        request.data["refresh_token"] = refresh_token

        exist_email = User.objects.filter(email=request.data["email"]).first()

        if exist_email:
            return Response(
                {
                    "success": False,
                    "message": "Пользователь с таким email уже существует",
                },
                status=status.HTTP_200_OK,
            )

        # сериализатор в формат python
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()
            # находится пользователь по email
            user = User.objects.get(email=request.data["email"])

            # сериализатор в формат json
            serializer_user = UserSerializer(user).data
            del serializer_user["password"]

            return Response(
                {
                    "success": True,
                    "accessToken": access_token,
                    "refreshToken": refresh_token,
                    "user": serializer_user,
                },
                status=status.HTTP_200_OK,
            )
        else:
            error_msg = ""
            # ошибка
            for key in serializer.errors:
                error_msg += serializer.errors[key][0]
            return Response(
                {"success": False, "message": error_msg},
                status=status.HTTP_200_OK,
            )


class CardViewSet(APIView):
    def get(self, request, format=None):
        # ищется карточка
        cards = Card.objects.all()
        # если карточки есть, то возвращается ответ с сериализатором и статусом 200 OK
        if cards:
            serializer_card = CardSerializer(cards, many=True)
            return Response(serializer_card.data, status=status.HTTP_200_OK)
        # если карточек нет, то возвращается ответ с ключом False и статусом 200 OK
        else:
            return Response(
                {
                    "success": False,
                    "message": "Карточки не найдены",
                },
                status=status.HTTP_200_OK,
            )


class UserViewSet(APIView):
    def get(self, request, format=None):
        print("o")
        # проверка токена, нужна для защищенной информации
        SafeJWTAuthentication.authenticate(self, request)
        user = request.user
        # если сериализатора нет, то возвращается ответ с ключом False со статусом 200 OK
        if user is None:
            return Response(
                {
                    "success": False,
                    "message": "Пользователь не найден",
                },
                status=status.HTTP_200_OK,
            )

        # если сериализатор есть, то возвращается ответ с данными сериализатора со статусом 200 OK
        else:
            return Response(user, status=status.HTTP_200_OK)

    def patch(self, request, format=None):
        print("i")
        if request.method == "PATCH":
            serializer_user, user = SafeJWTAuthentication.authenticate(self, request)
            print(serializer_user)
            name = request.data["name"]
            email = request.data["email"]
            # password = request.data["password"]

            serializer_user["name"] = name
            serializer_user["email"] = email
            # serializer_user["password"] = password

            serializer = UserSerializer(user, data=serializer_user, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "user": serializer_user,
                    },
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    {
                        "success": False,
                        "message": "Данные пользователя не обновились",
                    },
                    status=status.HTTP_200_OK,
                )


class UpdateTokenViewSet(APIView):
    def post(self, request, format=None):
        # достается из фронтенда token
        refresh = request.data["token"]
        # если при поиске по полученному с фронтенда refresh_token находится user в котором хранится refresh_token то значит ключи
        # одинаковые (проверку прошли)
        user = User.objects.get(refresh_token=refresh)
        # сериализуем user из python в json
        serializer = UserSerializer(user).data
        refresh_db = serializer["refresh_token"]
        # если пользователь не найден то возвращается ошибка
        if serializer["email"] is None or refresh_db != refresh:
            return Response(
                {
                    "success": False,
                    "message": "Токен не обновился",
                },
                status=status.HTTP_200_OK,
            )
        # если пользователь найден то генерируется access_token и возвращается access_token, refresh_token и success: True
        else:
            access_token = generate_access_token(serializer)
            return Response(
                {
                    "accessToken": access_token,
                    "refreshToken": refresh,
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )


class LoginView(APIView):
    def post(self, request, format=None):
        password = request.data["password"]
        email = request.data["email"]
        hashed_password = make_password(password=password, salt=SALT)

        # ищется пользователь по email
        user = User.objects.get(email=email)

        if user is None or user.password != hashed_password:
            return Response(
                {
                    "success": False,
                    "message": "Нет такого пользователя",
                },
                status=status.HTTP_200_OK,
            )

        else:
            access_token = generate_access_token(request.data)
            refresh_token = generate_refresh_token(request.data)
            serializer = UserSerializer(user).data
            del serializer["password"]
            return Response(
                {
                    "success": True,
                    "accessToken": access_token,
                    "refreshToken": refresh_token,
                    "user": serializer,
                },
                status=status.HTTP_200_OK,
            )


class LogoutViewSet(APIView):
    def post(self, request, format=None):
        refresh = request.data["token"]
        user = User.objects.get(refresh_token=refresh)
        serializer = UserSerializer(user).data
        serializer["refresh_token"] = ""
        print(serializer)

        serializer_update = UserSerializer(user, data=serializer, partial=True)
        if serializer_update.is_valid():
            serializer_update.save()
            return Response(
                {
                    "success": True,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "success": False,
                    "message": "Ошибка",
                },
                status=status.HTTP_200_OK,
            )
