from django.db import models

# Create your models here.

class Province(models.Model):
    province = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.province

class City(models.Model):
    city = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    def __str__(self):
        return self.city

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Store(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    manager = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    address = models.TextField(max_length=512)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
