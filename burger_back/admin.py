from django.contrib import admin
from .models import Card, User


class UserAdmin(admin.ModelAdmin):
    # обязательные поля в user
    list_display = ["_id", "email"]


class CardAdmin(admin.ModelAdmin):
    # обязательные поля в card
    list_display = ["_id", "name"]


admin.site.register(Card, CardAdmin)
admin.site.register(User, UserAdmin)
