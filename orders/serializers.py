from rest_framework import serializers
from .models import IndividualDiscount, GroupDiscount, Loan, Order, OrderItem
from accounts.serializers import CustomerSerializer, SellerSerializer
from inventory.serializers import InventorySerializer

class IndividualDiscountSerializer(serializers.ModelSerializer):
    customer_detail = CustomerSerializer(source='customer', read_only=True)

    class Meta:
        model = IndividualDiscount
        fields = ['id', 'active_date', 'customer', 'customer_detail']
        extra_kwargs = {
            'customer': {'write_only': True},
        }

class GroupDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupDiscount
        fields = ['id', 'used_count', 'max_use']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'prepayment']

class OrderItemSerializer(serializers.ModelSerializer):
    inventory_detail = InventorySerializer(source='inventory', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'inventory', 'inventory_detail', 'price']
        extra_kwargs = {
            'order': {'write_only': True},
            'inventory': {'write_only': True},
        }

class OrderSerializer(serializers.ModelSerializer):
    customer_detail = CustomerSerializer(source='customer', read_only=True)
    seller_detail = SellerSerializer(source='seller', read_only=True)
    loan_detail = LoanSerializer(source='loan', read_only=True)
    individual_discount_detail = IndividualDiscountSerializer(source='individual_discount', read_only=True)
    group_discount_detail = GroupDiscountSerializer(source='group_discount', read_only=True)
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_detail', 'seller', 'seller_detail',
                 'order_date', 'transaction_id', 'is_full_cash', 'loan', 'loan_detail',
                 'individual_discount', 'individual_discount_detail',
                 'group_discount', 'group_discount_detail', 'items', 'total_price']
        extra_kwargs = {
            'customer': {'write_only': True},
            'seller': {'write_only': True},
            'loan': {'write_only': True},
            'individual_discount': {'write_only': True},
            'group_discount': {'write_only': True},
        }

    def get_total_price(self, obj):
        return sum(item.price for item in obj.orderitem_set.all()) 