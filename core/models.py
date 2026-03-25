# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

# FR: User authentication and role-based access
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='cashier')

# FR: Customer management
class Customer(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# FR: Add, update, and delete product records
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, default='General')
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=10) # For low-stock notifications
    sku = models.CharField(max_length=100, blank=True, null=True, help_text="Barcode/SKU string for scanners")
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Tax or VAT percentage (e.g., 5.00 for 5%)")

    def __str__(self):
        return f"{self.name} - Stock: {self.stock_quantity}"

# FR: Process sales transactions
class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    cashier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
        ('mobile', 'Mobile Wallet'),
    )
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')

    def __str__(self):
        return f"Sale ID: {self.id} on {self.timestamp.strftime('%Y-%m-%d')}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT) # Don't delete product if in a sale
    quantity = models.PositiveIntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2) # Record price at the time of sale
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Per-item discount

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Sale {self.sale.id}"

# FR: Handle product returns
class Return(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    reason = models.TextField(blank=True, null=True)
    return_amount = models.DecimalField(max_digits=10, decimal_places=2)
    returned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Return: {self.quantity} x {self.product.name} from Sale #{self.sale.id}"