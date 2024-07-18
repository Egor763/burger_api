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
    path("ingredients", CardViewSet.as_view(), name="ingredients"),
    path("auth/user", UserViewSet.as_view(), name="user"),
    path("auth/register", RegistrationView.as_view(), name="register"),
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/token", UpdateTokenViewSet.as_view(), name="token"),
    path("auth/logout", LogoutViewSet.as_view(), name="logout"),
    path("password-reset", ForgotPasswordView.as_view(), name="forgot-password"),
    path("password-reset/reset", ResetPasswordView.as_view(), name="reset-password"),
]
