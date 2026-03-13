"""
URL configuration for posIms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ============ Authentication URLs ============
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login_page'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # ============ Dashboard ============
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ============ Product Management URLs ============
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # ============ Customer Management URLs ============
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    path('customers/<int:pk>/update/', views.customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    
    # ============ Sales URLs ============
    path('sales/transaction/', views.sales_transaction, name='sales_transaction'),
    path('sales/<int:pk>/receipt/', views.sales_receipt, name='sales_receipt'),
    path('sales/history/', views.sales_history, name='sales_history'),
    path('sales/<int:pk>/return/', views.process_return, name='process_return'),
    path('returns/', views.product_returns, name='product_returns'),
    
    # ============ Inventory URLs ============
    path('inventory/status/', views.inventory_status, name='inventory_status'),
    
    # ============ Report URLs ============
    path('reports/sales/', views.sales_report, name='sales_report'),
    path('reports/inventory/', views.inventory_report, name='inventory_report'),
]
