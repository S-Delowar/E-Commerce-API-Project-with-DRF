from django.test import TestCase
from django.contrib.auth import get_user_model
from cart.models import CartItem
from shop.models import Category, Product


# Tests for cart app
class CartModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='New Category')
        cls.product = Product.objects.create(
            name = 'Test Product',
            description = 'Test Product Description',
            price = 100.00,
            category = cls.category,
        )
        cls.user = get_user_model().objects.create_user(
            username="test_user",
            email = 'test_user@mail.com',
            password= 'testpass123'
        )
        
        cls.cart_item = CartItem.objects.create(
            user = cls.user,
            product = cls.product,
            quantity = 2
        )
        
        
    # Test for CartItem Model
    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.user, self.user)
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.quantity, 2)
        self.assertEqual(self.cart_item.total_price, 200.00)
        self.assertEqual(CartItem.objects.count(), 1)
        
    
    # def test_cart_item_creation_unauthorized_user(self):
    #     pass
    
    def test_cart_item_str(self):
        self.assertEqual(str(self.cart_item), 
                         'cartitem id- 1 - test_user - Test Product - (2)'
                         )
        