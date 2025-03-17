from django.db import models
from django.contrib.auth.models import AbstractUser

class Admin(AbstractUser):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)

    class Meta:
        db_table = 'admins'

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'companies'

class Province(models.Model):
    province = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'provinces'

class City(models.Model):
    city = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.CASCADE)

    class Meta:
        db_table = 'cities'
        unique_together = ('city', 'province')

class Store(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    manager = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=512)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'stores'

class Brand(models.Model):
    brand = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'brands'

class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'categories'

class PortionPlan(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    MCI_portion = models.FloatField()
    store_portion = models.FloatField()
    supplier_portion = models.FloatField()

    class Meta:
        db_table = 'portion_plans'

class Device(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    RAM = models.CharField(max_length=255, null=True)
    storage = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True)
    pack = models.CharField(max_length=255, null=True)
    network = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'devices'
        unique_together = ('category', 'brand', 'model')

class Supplier(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'suppliers' 