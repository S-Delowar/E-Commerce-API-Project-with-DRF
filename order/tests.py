from django.test import TestCase
from django.contrib.auth import get_user_model

from order.models import Order, OrderItem
from shop.models import Category, Product


# Order Models Tests
class OrderModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username='test_user1',
            email = 'test_user1@mail.com',
            password='test_pass1'
        )
        cls.order = Order.objects.create(
            user = cls.user1,
            total_price = 200.00,
            status = 'pending'
        )
        cls.category = Category.objects.create(
            name = 'Test Category'
        )
        cls.product = Product.objects.create(
            name = 'Test Product',
            category = cls.category,
            description = 'Test Description',
            price = 100.00
        )
        cls.order_item = OrderItem.objects.create(
            order = cls.order,
            product = cls.product,
            quantity = 3,
            price = 100.00
        )
        
    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user1)
        self.assertEqual(Order.objects.all().count(), 1)
        self.assertEqual(self.order.total_price, 200.00)
        
    def test_order_str_representation(self):
        self.assertEqual(str(self.order), f"Order {self.order.id} - {self.user1.username}")
        
    
    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 3)
        self.assertEqual(self.order_item.price, 100.00)
    
    def test_order_item_str_representation(self):
        self.assertEqual(str(self.order_item), f"{self.order_item.quantity} x {self.product.name} (Order {self.order.id})")
        