from django.urls import path, include

from .views import (
    CardViewSet,
    UserViewSet,
    RegistrationView,
    LoginView,
    UpdateTokenViewSet,
    LogoutViewSet,
)
from .password_views import ForgotPasswordView, ResetPasswordView

urlpatterns = [
    # карточки
    path("ingredients", CardViewSet.as_view(), name="ingredients"),
    # пользователь
    path("auth/user", UserViewSet.as_view(), name="user"),
    # регистрация
    path("auth/register", RegistrationView.as_view(), name="register"),
    # вход
    path("auth/login", LoginView.as_view(), name="login"),
    # токен
    path("auth/token", UpdateTokenViewSet.as_view(), name="token"),
    # выход
    path("auth/logout", LogoutViewSet.as_view(), name="logout"),
    # забыли пароль
    path("password-reset", ForgotPasswordView.as_view(), name="forgot-password"),
    # сброс пароля
    path("password-reset/reset", ResetPasswordView.as_view(), name="reset-password"),
]
