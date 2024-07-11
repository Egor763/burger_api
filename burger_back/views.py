from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Card
from .serializer import CardSerializer
from .tokens.auth import SafeJWTAuthentication


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
