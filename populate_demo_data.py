import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'posIms.settings')
django.setup()

from core.models import User, Product, Customer

# Clear existing demo data
print("Clearing existing demo data...")
User.objects.filter(username__in=['admin', 'manager', 'cashier']).delete()
Product.objects.all().delete()
Customer.objects.all().delete()

# Create users
print("Creating demo users...")
admin = User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='password',
    role='admin'
)
print(f"✓ Admin user created: admin / password")

manager = User.objects.create_user(
    username='manager',
    email='manager@example.com',
    password='password',
    role='manager',
    is_staff=True
)
print(f"✓ Manager user created: manager / password")

cashier = User.objects.create_user(
    username='cashier',
    email='cashier@example.com',
    password='password',
    role='cashier'
)
print(f"✓ Cashier user created: cashier / password")

# Create sample products
print("\nCreating sample products...")
products_data = [
    {'name': 'Laptop', 'category': 'Electronics', 'price': 999.99, 'stock': 15, 'threshold': 5},
    {'name': 'Mouse', 'category': 'Electronics', 'price': 29.99, 'stock': 50, 'threshold': 20},
    {'name': 'USB Cable', 'category': 'Accessories', 'price': 9.99, 'stock': 100, 'threshold': 50},
    {'name': 'Monitor', 'category': 'Electronics', 'price': 299.99, 'stock': 3, 'threshold': 5},
    {'name': 'Keyboard', 'category': 'Electronics', 'price': 79.99, 'stock': 25, 'threshold': 10},
    {'name': 'Desk Chair', 'category': 'Furniture', 'price': 199.99, 'stock': 8, 'threshold': 3},
    {'name': 'Desk Lamp', 'category': 'Accessories', 'price': 49.99, 'stock': 18, 'threshold': 10},
    {'name': 'Notebook', 'category': 'Stationery', 'price': 5.99, 'stock': 200, 'threshold': 50},
]

for product_data in products_data:
    Product.objects.create(
        name=product_data['name'],
        description=f"High quality {product_data['name'].lower()}",
        category=product_data['category'],
        selling_price=product_data['price'],
        stock_quantity=product_data['stock'],
        low_stock_threshold=product_data['threshold']
    )
    print(f"✓ {product_data['name']} - ${product_data['price']} (Stock: {product_data['stock']})")

# Create sample customers
print("\nCreating sample customers...")
customers_data = [
    {'name': 'Walk-in Customer', 'phone': '0000000000'},
    {'name': 'John Doe', 'phone': '555-1234'},
    {'name': 'Jane Smith', 'phone': '555-2345'},
    {'name': 'Bob Johnson', 'phone': '555-3456'},
    {'name': 'Alice Williams', 'phone': '555-4567'},
]

for customer_data in customers_data:
    Customer.objects.create(
        name=customer_data['name'],
        phone_number=customer_data['phone']
    )
    print(f"✓ {customer_data['name']} - {customer_data['phone']}")

print("\n" + "="*50)
print("✓ Demo data setup complete!")
print("="*50)
print("\nYou can now login with:")
print("  Admin:   admin / password")
print("  Manager: manager / password")
print("  Cashier: cashier / password")
print("\nAccess the system at: http://localhost:8000")
