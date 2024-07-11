from django.contrib import admin
from .models import Card, User


# class UserAdmin(admin.ModelAdmin):
#     # обязательные поля в user
#     list_display = ["id", "email"]


# class CardAdmin(admin.ModelAdmin):
#     # обязательные поля в card
#     list_display = ["id", "name"]


admin.site.register(Card)
admin.site.register(User)
