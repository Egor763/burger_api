from rest_framework import serializers

from .models import User, Card


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean(self)
        if User.objects.filter(email=cleaned_data.get("email")).exists():
            self.fields.add_error("email", "Эта почта уже зарегестрированна")
        return cleaned_data


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"
