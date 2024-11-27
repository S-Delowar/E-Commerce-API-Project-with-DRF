from django.db import models
from django.contrib.auth import get_user_model
from shop.models import Product

# class Cart(models.Model):
#     user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='cart')
#     created_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.id}"

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
    
#     def __str__(self):
#         return f"{self.cart.user.username} added {self.quantity} {self.product.name}"
    
    
# class WishListItem(models.Model):
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='wishlist')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)



# CartItem Model
class CartItem(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    
    def __str__(self):
        return f"cartitem id- {self.id} - {self.user.username} - {self.product.name} - ({self.quantity})"
    
    @property
    def total_price(self):
        return self.quantity * self.product.price
    