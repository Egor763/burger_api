from django.urls import path, include

from .views import (
    CardViewSet,
    UserViewSet,
    RegistrationView,
    LoginView,
    UpdateTokenViewSet,
    LogoutViewSet,
)

urlpatterns = [
    path("ingredients", CardViewSet.as_view(), name="ingredients"),
    path("auth/user", UserViewSet.as_view(), name="user"),
    path("auth/register", RegistrationView.as_view(), name="register"),
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/token", UpdateTokenViewSet.as_view(), name="token"),
    path("auth/logout", LogoutViewSet.as_view(), name="logout"),
]
