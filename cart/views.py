# from django.shortcuts import render
# from cart.models import Cart, CartItem, WishListItem
# from cart.serializers import CartItemSerializer, CartSerializer, WishListItemSerializer
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated

 
# # Cart ViewSet
# class CartViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartSerializer
    
#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.user)
    
#     # Automatically linking Cart to Logged in User
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
        

# # CartItem ViewSet
# class CartItemViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartItemSerializer
    
#     def get_queryset(self):
#         return CartItem.objects.filter(cart__user = self.request.user)
    
#     # Automatically linking CartItem to the Logged in User's Cart
#     def perform_create(self, serializer):
#         cart, created = Cart.objects.get_or_create(user = self.request.user)
#         serializer.save(cart=cart)
        

# # WishListItem ViewSet
# class WishListItemViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = WishListItemSerializer
    
#     def get_queryset(self):
#         return WishListItem.objects.filter(user = self.request.user)
    
        
# ===========================================================================================================


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from cart.models import CartItem
from cart.permissions import IsOwner
from cart.serializers import CartItemSerializer


# List or Create View for CartItem -[Get, Post]
# class CartItemListCreateView(generics.ListCreateAPIView):
#     serializer_class = CartItemSerializer
#     permission_classes = [IsAuthenticated,]
    
#     def get_queryset(self):
#         items = CartItem.objects.filter(user = self.request.user)
#         return items
    
#     def perform_create(self, serializer):
#         serializer.save(user = self.request.user)
        

# # Detail View of CartItem -[GET, PUT/PATCH, DELETE]
# class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
#     # queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#     permission_classes = [IsAuthenticated, IsOwner]
    
#     def get_queryset(self):
#         items = CartItem.objects.filter(user = self.request.user)
#         return items



# ViewSet for CartItem
class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        items = CartItem.objects.filter(user = self.request.user)
        return items
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)



# View for listing all cart-items to a dedicated cart api
class CartView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def get(self, request):
        cart_items = CartItem.objects.filter(user = request.user)
        items_serializer = CartItemSerializer(cart_items, many=True)
        total_price = sum(item.total_price for item in cart_items)
        
        return Response({
            'items': items_serializer.data,
            'total_price': total_price,
        })