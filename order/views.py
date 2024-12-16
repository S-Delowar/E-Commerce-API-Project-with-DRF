from django.shortcuts import render
from cart.models import CartItem
from order.models import Order, OrderItem
from order.serializers import OrderSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError




class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        return Order.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        cart_items = CartItem.objects.filter(user = self.request.user)
        
        if not cart_items.exists():
            ValidationError("Your cart is empty")
        
        total_price = sum(item.total_price for item in cart_items)
        
        # Create order
        order = serializer.save(
            user = self.request.user,
            total_price = total_price,
        )
        
        # Create order items
        order_items = [
            OrderItem(
                order = order,
                product = item.product,
                price = item.product.price,
                quantity = item.quantity,
            ) 
            for item in cart_items
        ]
        
        OrderItem.objects.bulk_create(order_items)
        cart_items.delete()