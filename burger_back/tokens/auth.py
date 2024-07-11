import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from ..models import User
from ..serializer import UserSerializer

# class CSRFCheck(CsrfViewMiddleware):
#     def _reject(self, request, reason):
#         # Return the failure reason instead of an HttpResponse
#         return reason


class SafeJWTAuthentication(BaseAuthentication):
    """
    custom authentication class for DRF and JWT
    https://github.com/encode/django-rest-framework/blob/master/rest_framework/authentication.py
    """

    def authenticate(self, request):
        # User = get_user_model()
        # добавление header Authorization
        authorization_heaader = request.headers.get("Authorization")

        # если нет authorization_header, то возвращается None
        if not authorization_heaader:
            return None
        try:
            # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
            access_token = authorization_heaader.split(" ")[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=["HS256"]
            )

        # вывод ошибки 403 истечение токена
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("токен истек")
        except IndexError:
            raise exceptions.AuthenticationFailed("Token prefix missing")

        # ищется id по первому пользователю
        user = User.objects.filter(id=payload["user_id"]).first()
        if user is None:
            # вывод ошибки пользователь не ненайден
            raise exceptions.AuthenticationFailed("Пользователь не найден")

        # self.enforce_csrf(request)
        serializer_user = UserSerializer(user).data
        request.user = serializer_user

        # print(request.user)
        return (serializer_user, user)

    # def enforce_csrf(self, request):
    #     """
    #     Enforce CSRF validation
    #     """
    #     check = CSRFCheck()
    #     # populates request.META['CSRF_COOKIE'], which is used in process_view()
    #     check.process_request(request)
    #     reason = check.process_view(request, None, (), {})
    #     print(reason)
    #     if reason:
    #         # CSRF failed, bail with explicit error message
    #         raise exceptions.PermissionDenied("CSRF Failed: %s" % reason)
