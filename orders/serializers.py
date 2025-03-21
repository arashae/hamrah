from rest_framework import serializers
from .models import IndividualDiscount, GroupDiscount, Loan, Order, OrderItem
from accounts.serializers import CustomerSerializer, UserSerializer
from inventory.serializers import SKUSerializer
from inventory.models import SKU
from accounts.models import Customer

class IndividualDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = IndividualDiscount
        fields = ['id', 'customer', 'sku', 'discount_percent', 'start_date', 'end_date']

class GroupDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDiscount
        fields = ['id', 'sku', 'discount_percent', 'start_date', 'end_date']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'customer', 'amount', 'installments', 'monthly_payment', 'start_date']

class OrderItemSerializer(serializers.ModelSerializer):
    sku = SKUSerializer(read_only=True)
    sku_id = serializers.PrimaryKeyRelatedField(
        queryset=SKU.objects.all(), source='sku', write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'sku', 'sku_id', 'quantity', 'unit_price', 'discount_percent']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_id', 'seller', 'items', 'total_amount',
                 'discount_amount', 'final_amount', 'status', 'created_at']
        read_only_fields = ['seller', 'total_amount', 'discount_amount', 'final_amount']

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data) 