# from rest_framework import serializers
# from .models import Cart, CartItem, WishListItem
# from shop.models import Product

# # Serializer for CartItem
# class CartItemSerializer(serializers.ModelSerializer):
#     product_name = serializers.ReadOnlyField(source="product.name")
#     product_price = serializers.ReadOnlyField(source="product.price")
    
#     class Meta:
#         model = CartItem
#         fields = ["id", "product", "product_name", "product_price", "quantity"]


# # Serializer for Cart
# class CartSerializer(serializers.ModelSerializer):
#     items = CartItemSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = Cart
#         fields = ["id", "user", "items", "created_at"]
        

# # Serializer for WishListItem
# class WishListItemSerializer(serializers.ModelSerializer):
#     product_name = serializers.ReadOnlyField(source='product.name')
    
#     class Meta:
#         model = WishListItem
#         fields = ['id', "product_name", "product"]




from rest_framework import serializers
from shop.serializers import ProductSerializer
from .models import CartItem


# CartItem Serializer
class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    product_details = ProductSerializer(source='product', read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_details', 'quantity', 'total_price']
        read_only_fields = ['user', 'total_price']
        