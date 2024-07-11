from django.urls import path, include

from .views import CardViewSet, UserViewSet

urlpatterns = [
    path("ingredients/", CardViewSet.as_view(), name="ingredients"),
    path("auth/user/", UserViewSet.as_view(), name="user"),
]
