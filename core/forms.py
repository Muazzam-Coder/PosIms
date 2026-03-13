# core/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Customer, Product, Sale, SaleItem


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'phone_number')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'category', 'selling_price', 'stock_quantity', 'low_stock_threshold')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Product Description'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'selling_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Selling Price', 'step': '0.01'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock Quantity'}),
            'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Low Stock Threshold'}),
        }


class SaleItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(stock_quantity__gt=0), 
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity'}))


class SaleForm(forms.ModelForm):
    customer_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Customer Name (leave blank for walk-in)'}))
    customer_phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (optional)'}))
    
    class Meta:
        model = Sale
        fields = ('discount_percentage',)
        widgets = {
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Discount %', 'step': '0.01'}),
        }


class SearchProductForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by name, category, or stock level'}))
    category_filter = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Filter by category'}))
    min_stock = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum stock'}))


class ReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    report_type = forms.ChoiceField(choices=[('sales', 'Sales Report'), ('inventory', 'Inventory Report')], 
                                     widget=forms.Select(attrs={'class': 'form-control'}))
