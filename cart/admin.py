from django.contrib import admin

from cart.models import CartItem

# from cart.models import Cart, CartItem, WishListItem


# class CartItemInline(admin.TabularInline):
#     model = CartItem
#     extra = 0
#     readonly_fields = ('product', 'quantity')
#     can_delete = False
    
    
# class CartAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'created_at')
#     search_fields = ('user__username',)
#     list_filter = ('created_at',)
#     inlines = [CartItemInline]


# class CartItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'cart', 'product', 'quantity')
#     search_fields = ('product__name', 'cart__user__username')
#     list_filter = ('cart',)
    
    
# class WishListItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'product')
#     search_fields = ('user__username', 'product__name')
#     list_filter = ('user',)
    
    
# Register models 
# admin.site.register(Cart, CartAdmin)
# admin.site.register(CartItem, CartItemAdmin)
# admin.site.register(WishListItem, WishListItemAdmin)


admin.site.register(CartItem)

