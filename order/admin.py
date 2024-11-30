from django.contrib import admin

from order.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'created_at', 'status']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username']
    
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    
admin.site.register(OrderItem, OrderItemAdmin)
