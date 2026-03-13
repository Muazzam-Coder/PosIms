# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum, Count, F
from django.utils import timezone
from datetime import datetime, timedelta

from .models import User, Customer, Product, Sale, SaleItem, Return
from .forms import (UserRegistrationForm, CustomerForm, ProductForm, 
                    SaleItemForm, SaleForm, SearchProductForm, ReportForm)


# ============ AUTHENTICATION VIEWS ============

def login_view(request):
    """Handle user login with role-based access."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def logout_view(request):
    """Handle user logout."""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


def register_view(request):
    """Admin-only user registration."""
    if not request.user.is_authenticated or request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


# ============ DASHBOARD VIEWS ============

@login_required
def dashboard(request):
    """Role-based dashboard with key metrics."""
    context = {}
    
    if request.user.role == 'admin':
        context['total_users'] = User.objects.count()
        context['total_customers'] = Customer.objects.count()
        context['total_products'] = Product.objects.count()
        context['total_sales'] = Sale.objects.count()
        return render(request, 'admin_dashboard.html', context)
    
    elif request.user.role == 'manager':
        today = timezone.now().date()
        context['today_sales'] = Sale.objects.filter(timestamp__date=today).count()
        context['today_revenue'] = Sale.objects.filter(timestamp__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        context['low_stock_products'] = Product.objects.filter(stock_quantity__lte=F('low_stock_threshold')).count()
        context['total_customers'] = Customer.objects.count()
        return render(request, 'manager_dashboard.html', context)
    
    else:  # cashier
        context['pending_sales'] = 0  # Can track temporary sales
        return render(request, 'cashier_dashboard.html', context)


# ============ PRODUCT MANAGEMENT VIEWS ============

@login_required
def product_list(request):
    """List all products with search and filter functionality."""
    if request.user.role == 'cashier':
        messages.error(request, 'Access denied. Manager or Admin only.')
        return redirect('dashboard')
    
    form = SearchProductForm(request.GET or None)
    products = Product.objects.all()
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category_filter')
        min_stock = form.cleaned_data.get('min_stock')
        
        if search:
            products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if category:
            products = products.filter(category__icontains=category)
        if min_stock is not None:
            products = products.filter(stock_quantity__gte=min_stock)
    
    # Highlight low stock items
    for product in products:
        product.is_low_stock = product.stock_quantity <= product.low_stock_threshold
    
    context = {'products': products, 'form': form}
    return render(request, 'product_list.html', context)


@login_required
def product_create(request):
    """Add a new product."""
    if request.user.role not in ['admin', 'manager']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def product_update(request, pk):
    """Update product details."""
    if request.user.role not in ['admin', 'manager']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product_form.html', {'form': form, 'title': 'Update Product'})


@login_required
def product_delete(request, pk):
    """Delete a product."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard')
    
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')
    
    return render(request, 'product_confirm_delete.html', {'product': product})


# ============ CUSTOMER MANAGEMENT VIEWS ============

@login_required
def customer_list(request):
    """List all customers."""
    if request.user.role == 'cashier':
        messages.error(request, 'Access denied. Manager or Admin only.')
        return redirect('dashboard')
    
    customers = Customer.objects.all().order_by('-created_at')
    context = {'customers': customers}
    return render(request, 'customer_list.html', context)


@login_required
def customer_create(request):
    """Add a new customer."""
    if request.user.role not in ['admin', 'manager', 'cashier']:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    
    return render(request, 'customer_form.html', {'form': form, 'title': 'Add Customer'})


@login_required
def customer_update(request, pk):
    """Update customer information."""
    if request.user.role not in ['admin', 'manager']:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer updated successfully.')
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'customer_form.html', {'form': form, 'title': 'Update Customer'})


@login_required
def customer_delete(request, pk):
    """Delete a customer."""
    if request.user.role != 'admin':
        messages.error(request, 'Access denied. Admin only.')
        return redirect('dashboard')
    
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully.')
        return redirect('customer_list')
    
    return render(request, 'customer_confirm_delete.html', {'customer': customer})


# ============ SALES VIEWS ============

@login_required
def sales_transaction(request):
    """Process a new sales transaction."""
    if request.user.role != 'cashier':
        messages.error(request, 'Access denied. Cashiers only.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            # Validate stock before creating sale
            products = request.POST.getlist('product_id')
            quantities = request.POST.getlist('quantity')
            
            # Check if all products have enough stock
            stock_issues = []
            for product_id, quantity in zip(products, quantities):
                if product_id and quantity:
                    product = get_object_or_404(Product, pk=product_id)
                    quantity = int(quantity)
                    
                    if product.stock_quantity < quantity:
                        stock_issues.append(
                            f'{product.name}: Only {product.stock_quantity} in stock, '
                            f'trying to sell {quantity}'
                        )
            
            if stock_issues:
                messages.error(request, 'Insufficient stock: ' + ' | '.join(stock_issues))
                form = SaleForm()
                products_list = Product.objects.all()
                return render(request, 'sales_transaction.html', {
                    'form': form,
                    'products': products_list
                })
            
            # Get or create customer
            customer_name = form.cleaned_data.get('customer_name')
            customer_phone = form.cleaned_data.get('customer_phone')
            
            if customer_name:
                customer, _ = Customer.objects.get_or_create(
                    name=customer_name,
                    defaults={'phone_number': customer_phone or ''}
                )
            else:
                # Default random/walk-in customer
                customer, _ = Customer.objects.get_or_create(
                    name='Walk-in Customer',
                    defaults={'phone_number': '0000000000'}
                )
            
            # Create sale
            discount_percentage = form.cleaned_data.get('discount_percentage', 0)
            total_amount = request.POST.get('total_amount')
            
            if total_amount:
                sale = Sale.objects.create(
                    customer=customer,
                    cashier=request.user,
                    total_amount=total_amount,
                    discount_percentage=discount_percentage
                )
                
                # Process sale items and update inventory
                discount_amounts = request.POST.getlist('discount_amount')
                for product_id, quantity, discount_amount in zip(products, quantities, discount_amounts):
                    if product_id and quantity:
                        product = get_object_or_404(Product, pk=product_id)
                        quantity = int(quantity)
                        discount_amt = float(discount_amount) if discount_amount else 0
                        
                        SaleItem.objects.create(
                            sale=sale,
                            product=product,
                            quantity=quantity,
                            price_at_sale=product.selling_price,
                            discount_amount=discount_amt
                        )
                        
                        # Update inventory
                        product.stock_quantity -= quantity
                        product.save()
                
                messages.success(request, f'Sale #{sale.id} processed successfully.')
                return redirect('sales_receipt', pk=sale.id)
    else:
        form = SaleForm()
    
    products = Product.objects.filter(stock_quantity__gt=0)
    context = {'form': form, 'products': products}
    return render(request, 'sales_transaction.html', context)


@login_required
def sales_receipt(request, pk):
    """Display receipt for a completed sale."""
    sale = get_object_or_404(Sale, pk=pk)
    
    if request.user.role == 'cashier' and sale.cashier != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    # Calculate subtotal and discount amount from sale items
    sale_items = SaleItem.objects.filter(sale=sale)
    subtotal = sum(item.quantity * item.price_at_sale for item in sale_items)
    
    # Calculate discount amount
    discount_amount = subtotal * (sale.discount_percentage / 100) if sale.discount_percentage > 0 else 0
    
    context = {
        'sale': sale,
        'subtotal': subtotal,
        'discount_amount': discount_amount,
        'items': sale_items
    }
    return render(request, 'sales_receipt.html', context)


@login_required
def sales_history(request):
    """View sales history."""
    if request.user.role == 'cashier':
        sales = Sale.objects.filter(cashier=request.user).order_by('-timestamp')
    else:
        sales = Sale.objects.all().order_by('-timestamp')
    
    context = {'sales': sales}
    return render(request, 'sales_history.html', context)


# ============ PRODUCT RETURN VIEWS ============

@login_required
def product_returns(request):
    """View and manage product returns."""
    if request.user.role == 'cashier':
        returns = Return.objects.filter(returned_by=request.user).order_by('-created_at')
    else:
        returns = Return.objects.all().order_by('-created_at')
    
    context = {'returns': returns}
    return render(request, 'product_returns.html', context)


@login_required
def process_return(request, pk):
    """Process a product return."""
    sale = get_object_or_404(Sale, pk=pk)
    
    if request.user.role == 'cashier' and sale.cashier != request.user:
        messages.error(request, 'Access denied.')
        return redirect('dashboard')
    
    sale_items = sale.items.all()
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        reason = request.POST.get('reason', '')
        
        # Get the sale item to find the price
        sale_item = get_object_or_404(SaleItem, sale=sale, product_id=product_id)
        return_amount = (sale_item.price_at_sale * quantity) - sale_item.discount_amount
        
        # Create return record
        Return.objects.create(
            sale=sale,
            product_id=product_id,
            quantity=quantity,
            reason=reason,
            return_amount=return_amount,
            returned_by=request.user
        )
        
        # Update inventory - add back to stock
        product = Product.objects.get(pk=product_id)
        product.stock_quantity += quantity
        product.save()
        
        messages.success(request, f'Return processed successfully. ${return_amount} refunded.')
        return redirect('sales_receipt', pk=sale.id)
    
    context = {'sale': sale, 'sale_items': sale_items}
    return render(request, 'process_return.html', context)


# ============ INVENTORY VIEWS ============

@login_required
def inventory_status(request):
    """View inventory status and low-stock alerts."""
    if request.user.role == 'cashier':
        messages.error(request, 'Access denied. Manager or Admin only.')
        return redirect('dashboard')
    
    products = Product.objects.all()
    low_stock_products = products.filter(stock_quantity__lte=F('low_stock_threshold'))
    
    context = {
        'products': products,
        'low_stock_products': low_stock_products,
        'low_stock_count': low_stock_products.count()
    }
    return render(request, 'inventory_status.html', context)


# ============ REPORT VIEWS ============

@login_required
def sales_report(request):
    """Generate sales reports for a given period with quantity details."""
    if request.user.role == 'cashier':
        messages.error(request, 'Access denied. Manager or Admin only.')
        return redirect('dashboard')
    
    form = ReportForm(request.GET or None)
    sales = Sale.objects.all()
    sales_items = SaleItem.objects.all()
    report_data = None
    product_summary = None
    
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        
        # Combine dates with time for proper filtering
        start_datetime = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        end_datetime = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
        
        sales = sales.filter(timestamp__range=[start_datetime, end_datetime])
        sales_items = sales_items.filter(sale__timestamp__range=[start_datetime, end_datetime])
        
        # Product-level summary with quantities
        product_summary = {}
        for item in sales_items:
            if item.product.id not in product_summary:
                product_summary[item.product.id] = {
                    'product_name': item.product.name,
                    'total_quantity': 0,
                    'total_revenue': 0,
                    'num_items': 0
                }
            product_summary[item.product.id]['total_quantity'] += item.quantity
            product_summary[item.product.id]['total_revenue'] += (item.quantity * item.price_at_sale - item.discount_amount)
            product_summary[item.product.id]['num_items'] += 1
        
        report_data = {
            'total_sales': sales.count(),
            'total_revenue': sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'average_sale': sales.aggregate(avg=Sum('total_amount') / Count('id'))['avg'] or 0,
            'total_discount': sales.aggregate(Sum('discount_percentage'))['discount_percentage__sum'] or 0,
            'total_quantity_sold': sales_items.aggregate(Sum('quantity'))['quantity__sum'] or 0,
            'num_unique_items': sales_items.values('product').distinct().count(),
            'period': f"{start_date} to {end_date}"
        }
    
    context = {
        'form': form,
        'sales': sales,
        'report_data': report_data,
        'product_summary': product_summary
    }
    return render(request, 'sales_report.html', context)


@login_required
def inventory_report(request):
    """Generate inventory reports."""
    if request.user.role == 'cashier':
        messages.error(request, 'Access denied. Manager or Admin only.')
        return redirect('dashboard')
    
    products = Product.objects.all()
    
    report_data = {
        'total_products': products.count(),
        'total_stock_value': sum(p.stock_quantity * p.selling_price for p in products),
        'low_stock_count': products.filter(stock_quantity__lte=F('low_stock_threshold')).count(),
        'out_of_stock_count': products.filter(stock_quantity=0).count(),
    }
    
    context = {'products': products, 'report_data': report_data}
    return render(request, 'inventory_report.html', context)
