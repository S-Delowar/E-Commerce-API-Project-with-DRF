from django.urls import path, include

# from cart.views import CartItemDetailView, CartItemListCreateView, CartView

from cart.views import CartItemViewSet, CartView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'cart/items', CartItemViewSet, basename='cart-item')
# router.register(r'cart-items', CartItemViewSet, basename='cart-items')
# router.register(r'wishlist', WishListItemViewSet, basename='wishlist')

# urlpatterns = [
#     path('', include(router.urls))
# ]


# urlpatterns = [
#     path('cart/items/', CartItemListCreateView.as_view(), name='cart-items'),
#     path('cart/items/<int:pk>/', CartItemDetailView.as_view(), name='cartitem-detail'),
#     path('cart/', CartView.as_view(), name='cart')
    
# ]

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view(), name='cart'),
]