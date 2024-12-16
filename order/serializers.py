from order.models import Order, OrderItem
from rest_framework import serializers


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']
        

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only = True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'items', 'total_price']
        read_only_fields = ['user', 'created_at', 'total_price']