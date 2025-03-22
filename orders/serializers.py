from rest_framework import serializers
from .models import IndividualDiscount, GroupDiscount, Loan, Order, OrderItem
from accounts.serializers import CustomerSerializer, UserSerializer
from inventory.serializers import SKUSerializer
from inventory.models import SKU
from accounts.models import Customer

class IndividualDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualDiscount
        fields = ['id', 'customer', 'active_date']

class GroupDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDiscount
        fields = ['id', 'used_count', 'max_use']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'prepayment', 'amount', 'installments', 'monthly_payment', 'start_date']

class OrderItemSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(source='inventory.sku', read_only=True)
    sku_id = serializers.IntegerField(source='inventory.id', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'inventory', 'price', 'quantity', 'sku', 'sku_id']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    customer_id = serializers.IntegerField(source='customer.id', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_id', 'seller', 'items', 'order_date', 'transaction_id', 'is_full_cash', 'loan', 'individual_discount', 'group_discount', 'status']
        read_only_fields = ['seller', 'order_date', 'status']

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data) 