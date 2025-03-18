from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'سوپر ادمین'),
        ('store_admin', 'ادمین فروشگاه'),
        ('seller', 'فروشنده'),
        ('warehouse', 'انباردار'),
        ('supplier', 'تامین کننده'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)
    national_code = models.CharField(max_length=10)
    store = models.ForeignKey('management.Store', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return f"{self.full_name} - {self.get_role_display()}"

    def save(self, *args, **kwargs):
        # اگر کاربر جدید است و رمز عبور تنظیم نشده
        if not self.pk and not self.password:
            self.set_password(self.password)
        super().save(*args, **kwargs)

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
