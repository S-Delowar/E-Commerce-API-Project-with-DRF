from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from cart.models import CartItem
from rest_framework.test import APITestCase
from rest_framework import status

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
        
        

# ============================== Tests for Order APIs =======================
class OrderAPIsTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = get_user_model().objects.create_user(
            username='testuser1', email='testuser1@mail.com', password='user1pass'
        )
        cls.user2 = get_user_model().objects.create_user(
            username='testuser2', email='testuser2@mail.com', password='user2pass'
        )
        cls.category1 = Category.objects.create(name='First Category')
        cls.category2 = Category.objects.create(name='Second Category')
        cls.product1 = Product.objects.create(
            name='First Product', description='First Description', price=30, category=cls.category1
        )
        cls.product2 = Product.objects.create(
            name='Second Product', description='Second Description', price=10, category=cls.category2
        )
        cls.product3 = Product.objects.create(
            name='Third Product', description='Third Description', price=65, category=cls.category2
        )
        cls.product4 = Product.objects.create(
            name='Fourth Product', description='Fourth Description', price=25, category=cls.category2
        )
        cls.cart_item1 = CartItem.objects.create(
            user = cls.user1, product = cls.product1, quantity = 5
        )
        cls.cart_item2 = CartItem.objects.create(
            user = cls.user2, product = cls.product2, quantity = 2
        )
        cls.cart_item3 = CartItem.objects.create(
            user = cls.user1, product = cls.product3, quantity = 10
        )
        cls.cart_item4 = CartItem.objects.create(
            user = cls.user2, product = cls.product4, quantity = 4
        )
        

    def test_create_order(self):
        """Test Creating an order from cart items"""
        self.client.login(username=self.user1.username, email=self.user1.email, password='user1pass')

        response = self.client.post(reverse('order-list'), {})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the order is created
        order = Order.objects.get(user=self.user1)
        self.assertEqual(order.total_price, 800)
        self.assertEqual(order.status, 'pending')
        
        # Verify the order items are created
        self.assertEqual(order.items.count(), 2)
        order_item1 = order.items.get(product=self.product1)
        order_item2 = order.items.get(product=self.product3)
        
        self.assertEqual(order_item1.quantity, 5)
        self.assertEqual(order_item1.price, 30)
        
        self.assertEqual(order_item2.quantity, 10)
        self.assertEqual(order_item2.price, 65)
        
        # Verify cart items are cleared
        self.assertFalse(CartItem.objects.filter(user=self.user1).exists())

    
    def test_create_order_with_empty_cart(self):
        self.client.login(username=self.user1.username, email=self.user1.email, password='user1pass')
        
        # Clear the cart
        CartItem.objects.filter(user=self.user1).delete()
        
        response = self.client.post(reverse('order-list'), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Your cart is empty", response.data)
    
    
    def test_update_order_not_allowed(self):
        order = Order.objects.create(user=self.user1, total_price=120)
        
        self.client.login(username=self.user1.username, email=self.user1.email, password='user1pass')

        response = self.client.put(reverse('order-detail', kwargs={'pk': order.id}), 
                                   {
                                       'status': 'completed'
                                   })
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    
    def test_delete_order_not_allowed(self):
        order = Order.objects.create(user=self.user1, total_price=120)
        self.client.login(username=self.user1.username, email=self.user1.email, password='user1pass')
        response = self.client.delete(reverse('order-detail', kwargs={'pk': order.id}))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

