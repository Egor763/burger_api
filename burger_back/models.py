from django.db import models

import uuid


class Card(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=300)
    price = models.CharField(max_length=50)
    image_mobile = models.CharField(max_length=300, blank=True, null=True)
    image_large = models.CharField(max_length=300, blank=True, null=True)
    type = models.CharField(max_length=15)
    proteins = models.IntegerField()
    fat = models.IntegerField()
    carbohydrates = models.IntegerField()
    calories = models.IntegerField()
    price = models.IntegerField()


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=300, blank=True, null=True)
    refresh_token = models.CharField(max_length=250, blank=True, null=True)
