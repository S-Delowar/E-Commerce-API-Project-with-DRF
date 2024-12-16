from django.urls import path, include
from order.views import OrderViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]
