from django.db import models

# Create your models here.

class Brand(models.Model):
    brand = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.brand

class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category

class Device(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.CharField(max_length=255)
    RAM = models.CharField(max_length=255)
    storage = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    pack = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

class Supplier(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class Guarantee(models.Model):
    guarantee = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.guarantee

class PortionPlan(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    MCI_portion = models.FloatField()
    store_portion = models.FloatField()
    supplier_portion = models.FloatField()

    def __str__(self):
        return f"{self.category} - MCI: {self.MCI_portion}%"

class SKU(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.IntegerField()
    guarantee = models.ForeignKey(Guarantee, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    detail = models.TextField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f"{self.device} - {self.supplier}"

class Inventory(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)
    SKU = models.ForeignKey(SKU, on_delete=models.CASCADE)
    IMEI = models.CharField(max_length=15, null=True, blank=True)
    receive_date = models.DateTimeField(null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    discount_rate = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.store} - {self.SKU}"
