# core/serializers.py

from rest_framework import serializers
from .models import User, Customer, Product, Sale, SaleItem, Return

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_at_sale', 'discount_amount']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    customer_name = serializers.ReadOnlyField(source='customer.name')
    cashier_username = serializers.ReadOnlyField(source='cashier.username')

    class Meta:
        model = Sale
        fields = [
            'id', 'customer', 'customer_name', 'cashier', 'cashier_username', 
            'timestamp', 'total_amount', 'discount_percentage', 'tax_amount', 
            'payment_method', 'items'
        ]

class ReturnSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    returned_by_username = serializers.ReadOnlyField(source='returned_by.username')

    class Meta:
        model = Return
        fields = '__all__'
