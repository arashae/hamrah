from django.db import models

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
    prepayment = models.IntegerField()

    def __str__(self):
        return f"Prepayment: {self.prepayment}"

class Order(models.Model):
    customer = models.ForeignKey('accounts.Customer', on_delete=models.CASCADE)
    seller = models.ForeignKey('accounts.Seller', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=12)
    is_full_cash = models.BooleanField(default=True)
    loan = models.ForeignKey(Loan, on_delete=models.SET_NULL, null=True, blank=True)
    individual_discount = models.ForeignKey(IndividualDiscount, on_delete=models.SET_NULL, null=True, blank=True)
    group_discount = models.ForeignKey(GroupDiscount, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.customer} - {self.transaction_id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    inventory = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.order} - {self.inventory}"
