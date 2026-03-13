from django.contrib import admin
from .models import User, Customer, Product, Sale, SaleItem, Return


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role',)
    search_fields = ('username', 'email')


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'created_at')
    search_fields = ('name', 'phone_number')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'selling_price', 'stock_quantity')
    search_fields = ('name', 'category')
    list_filter = ('category',)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'cashier', 'total_amount', 'timestamp')
    list_filter = ('timestamp',)


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'price_at_sale', 'discount_amount')


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):
    list_display = ('sale', 'product', 'quantity', 'return_amount', 'returned_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'sale__id')
