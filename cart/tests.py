from ast import arg
from os import name
from unicodedata import category
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from cart.models import CartItem
from shop.models import Category, Product

from rest_framework.test import APITestCase
from rest_framework import status



# ============================== Tests for CartItem Models ======================

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
        
    def test_cart_item_str(self):
        self.assertEqual(str(self.cart_item), f'cartitem id- {self.cart_item.id} - test_user - Test Product - (2)')
        
        
        
# ============================== Tests for CartItem APIs =======================

class CartItemAPIsTests(APITestCase):
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
            name='First Product', description='First Description', price=300, category=cls.category1
        )
        cls.product2 = Product.objects.create(
            name='Second Product', description='Second Description', price=100, category=cls.category2
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
            user = cls.user2, product = cls.product4, quantity = 5
        )
        
        
        
    # Test for getting cart-item list
    def test_get_cartitem_list(self):
        #anonymous user
        response = self.client.get(reverse('cart-item-list'), arg=[self.user1.id])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Login as test user-1
        self.client.login(username='testuser1', email='testuser1@mail.com', password='user1pass')
        response = self.client.get(reverse('cart-item-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertContains(response.data, self.cart_item1)
        # self.assertIn(response.data, self.cart_item2)
        cart_item_ids = [item['id'] for item in response.data] 
        self.assertIn(self.cart_item1.id, cart_item_ids)  
        self.assertNotIn(self.cart_item2.id, cart_item_ids) 
        self.client.logout()
        # print('cart item list test ok - tet user 1')
        
        # Login as test user-2
        self.client.login(username='testuser2', email='testuser2@mail.com', password='user2pass')
        response = self.client.get(reverse('cart-item-list'))
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item_ids = [item["id"] for item in response.data]
        self.assertNotIn(self.cart_item1.id, cart_item_ids)
        self.assertIn(self.cart_item2.id, cart_item_ids)
        # print('cart item list test ok for user-2')
    
        
        # Note -  Not working:
        # self.assertContains(response.data, self.cart_item1)
        # self.assertIn(response.data, self.cart_item2)
        '''self.assertIn expects the first argument to be a single item that can be checked for membership in the second argument (an iterable). response.data is likely a list of serialized cart items, while self.cart_item1 is a model instance '''
        '''And self.assertContains is specifically designed for testing the presence of a string or HTML fragment in the response content, not for checking the inclusion of an object in a serialized response like response.data
        '''    
        ''' So the solution is: 
            check cart-item ids in the items of the response data   
            
            cart_item_ids = [item['id'] for item in response.data] 
            self.assertIn(self.cart_item1.id, cart_item_ids)  
            self.assertNotIn(self.cart_item2.id, cart_item_ids) 
            
            or
            cart_items = response.data
            self.assertTrue(any(item['id'] == self.cart_item1.id for item in cart_items)) 
            self.assertFalse(any(item['id'] == self.cart_item2.id for item in cart_items)) 
        '''

        
    
    # Test for getting single cart-item
    def test_get_cart_item_detail_by_id(self):
        # anonymous user
        response = self.client.get(reverse('cart-item-detail', args=[self.cart_item1.id]))
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Logged in user get own items
        self.client.login(username='testuser1', email='testuser1@mail.com', password='user1pass')
        response = self.client.get(reverse('cart-item-detail', args=[self.cart_item1.id]))
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # get other's items
        response = self.client.get(reverse('cart-item-detail', args=[self.cart_item2.id]))
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
    # Test for patching a cart-item
    def test_update_cart_item_by_id(self):
        new_data = {
            "quantity": 333
        }
        
        # login user
        self.client.login(username='testuser1', email='testuser1@mail.com', password='user1pass')

        # updating own cart-item
        response = self.client.patch(reverse('cart-item-detail', args=[self.cart_item1.id]), new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.cart_item1.refresh_from_db()
        self.assertEqual(self.cart_item1.quantity, 333)
        
        # updating other's cart-item
        response = self.client.patch(reverse('cart-item-detail', args=[self.cart_item2.id]), new_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.cart_item2.refresh_from_db()
        self.assertEqual(self.cart_item2.quantity, 2)
        # print('test ok - updating others cart-item')  
    
    
    # Test for deleting a cart-item
    def test_delete_cart_item_by_id(self):
        # login user
        self.client.login(username='testuser1', email='testuser1@mail.com', password='user1pass')

        # delete own cart-item
        response = self.client.delete(reverse('cart-item-detail', args=[self.cart_item1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # verifying the item is deleted or not
        response = self.client.get(reverse('cart-item-detail', args=[self.cart_item1.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        
        # delete other's cart-item
        response = self.client.patch(reverse('cart-item-detail', args=[self.cart_item2.id]))
        # print(f"delete cartitem code - {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # print('test - delete cart item ok')
    
    
    # Test for the dedicated cart
    def test_dedicated_cart(self):
        # Anonymous user
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # login as user 2
        self.client.login(username='testuser2', email='testuser2@mail.com', password='user2pass')
        response = self.client.get(reverse('cart'))
        # print(f"cart response data user 2: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 2)
        user_ids = [item["user"] for item in response.data["items"]]
        # print(user_ids)
        self.assertTrue(all(user_id == self.user2.id for user_id in user_ids))
        
        

        
        
        
            
        
    