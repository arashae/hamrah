from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'سوپر ادمین'),
        ('store_admin', 'ادمین فروشگاه'),
        ('seller', 'فروشنده'),
        ('warehouse', 'انباردار'),
        ('supplier', 'تامین کننده'),
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
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
        if not self.pk and not self.has_usable_password():
            self.set_password(self.password)
        super().save(*args, **kwargs)

class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    national_code = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=11)
    gender = models.BooleanField()
    id_card = models.CharField(max_length=10)
    address = models.TextField(max_length=512)
    postal_code = models.CharField(max_length=10)

    class Meta:
        db_table = 'customers'
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Seller(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    store = models.ForeignKey('management.Store', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sellers'
        verbose_name = 'فروشنده'
        verbose_name_plural = 'فروشندگان'

    def __str__(self):
        return self.name

class StoreAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store = models.ForeignKey('management.Store', on_delete=models.CASCADE)

    class Meta:
        db_table = 'store_admins'
        verbose_name = 'ادمین فروشگاه'
        verbose_name_plural = 'ادمین‌های فروشگاه'

    def __str__(self):
        return f"{self.user.full_name} - {self.store.name}"

class StoreUser(models.Model):
    ROLE_CHOICES = (
        ('seller', 'فروشنده'),
        ('warehouse', 'انباردار'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store = models.ForeignKey('management.Store', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        db_table = 'store_users'
        verbose_name = 'کاربر فروشگاه'
        verbose_name_plural = 'کاربران فروشگاه'

    def __str__(self):
        return f"{self.user.full_name} - {self.get_role_display()} - {self.store.name}"
