# core/admin.py

from django.contrib import admin
from .models import User, Customer, Product, Sale, SaleItem

# We can customize the admin interface here later if needed

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(SaleItem)