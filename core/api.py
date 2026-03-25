# core/api.py

from rest_framework import viewsets, permissions
from .models import Customer, Product, Sale, Return
from .serializers import CustomerSerializer, ProductSerializer, SaleSerializer, ReturnSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be viewed or edited.
    """
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class SaleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sales to be viewed or edited.
    """
    queryset = Sale.objects.all().order_by('-timestamp')
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReturnViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows returns to be viewed or edited.
    """
    queryset = Return.objects.all().order_by('-created_at')
    serializer_class = ReturnSerializer
    permission_classes = [permissions.IsAuthenticated]
