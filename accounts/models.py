from django.db import models
from django.contrib.auth.models import AbstractUser

class Admin(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    national_code = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=11)
    gender = models.BooleanField()
    id_card = models.CharField(max_length=10)
    address = models.TextField(max_length=512)
    postal_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Seller(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
