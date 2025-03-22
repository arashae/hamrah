from django.db import models
from django.utils import timezone

# Create your models here.

class IndividualDiscount(models.Model):
    active_date = models.DateTimeField()
    customer = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.customer} - {self.active_date}"

class GroupDiscount(models.Model):
    used_count = models.IntegerField()
    max_use = models.IntegerField()

    def __str__(self):
        return f"Used: {self.used_count}/{self.max_use}"

class Loan(models.Model):
    prepayment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    installments = models.IntegerField(default=1)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    start_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Loan {self.id} - {self.amount} ({self.installments} installments)"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('processing', 'در حال پردازش'),
        ('completed', 'تکمیل شده'),
        ('cancelled', 'لغو شده'),
    ]

    customer = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)
    seller = models.ForeignKey('accounts.Seller', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=12)
    is_full_cash = models.BooleanField(default=True)
    loan = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True, blank=True)
    individual_discount = models.ForeignKey(IndividualDiscount, on_delete=models.SET_NULL, null=True, blank=True)
    group_discount = models.ForeignKey(GroupDiscount, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.customer} - {self.transaction_id} ({self.get_status_display()})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    inventory = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.order} - {self.inventory} (x{self.quantity})"
