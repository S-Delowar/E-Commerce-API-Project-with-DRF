from django.test import TestCase
from shop.models import Category, Product, ProductImage
from uuid import UUID
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status



# ================================ Tests for Models ===============================
# Tests for Shop related Models
class ShopModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='New Category')
        cls.product = Product.objects.create(
            name = 'Test Product',
            description = 'Test Product Description',
            price = 255.55,
            category = cls.category,
        )
        
        cls.product_image = ProductImage.objects.create(
            product = cls.product,
            image = SimpleUploadedFile(
                'test_image.jpg',
                b'file_content',
                content_type='image/jpeg'
            ),
        )
           
    # Tests for Category Model
    def test_category_creation(self):
        self.assertEqual(self.category.name, 'New Category')
        self.assertEqual(self.category.slug, 'new-category')
        
    def test_category_str(self):
        self.assertEqual(str(self.category), 'New Category')
        
    
    # Tests for Product Model
    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.description, 'Test Product Description')
        self.assertEqual(self.product.price, 255.55)
        self.assertEqual(self.product.category, self.category)
        self.assertIsInstance(self.product.id, UUID)
        
    def test_product_str(self):
        self.assertEqual(str(self.product), 'Test Product')
        
    
    # Tests for ProductImage  Model
    def test_product_image_creation(self):
        # print(f"image name - {self.product_image.image.name}")
        self.assertEqual(self.product_image.product, self.product)
        self.assertTrue(self.product_image.image.name.startswith("product_images/test_image")) 
    
    def test_image_str(self):
        self.assertEqual(str(self.product_image), 'Image for Test Product')
        
        

#================================= Tests for API Endpoints ============================= 

# Tests for Category APIs
# -----------------------
class CategoryAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category1 = Category.objects.create(name="New Category 1")
        cls.category2 = Category.objects.create(name="New Category 2")
        cls.staff_user = get_user_model().objects.create_user(
            username='staff_user', 
            email='staff_user@mail.com',
            password='staffpass123',
            is_staff = True,
        )
        cls.non_staff_user = get_user_model().objects.create_user(
            username='non_staff_user', 
            email='non_staff_user@mail.com',
            password='nonstaffpass123',
            is_staff=False
        )
        
    # Test for getting category list for anyone   
    def test_get_category_list(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'New Category 1')
     
             
    # Test for posting category anonymous, non-staff and staff user
    def test_post_category(self):
        new_category_data = {"name": "Latest Category"}
        
        # Anonymous User
        response = self.client.post(reverse('category-list'), new_category_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Non-staff User
        self.client.login(username='non_staff_user', email="non_staff_user@mail.com", password="nonstaffpass123")
        response = self.client.post(reverse('category-list'), new_category_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()
        
        # Staff user
        self.client.login(username='staff_user', email="staff_user@mail.com", password="staffpass123")
        response = self.client.post(reverse('category-list'), new_category_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.last().name, 'Latest Category')
        self.assertEqual(Category.objects.last().slug, 'latest-category')
        
    
        
    # Test for getting single category for anyone           
    def test_get_category_by_id(self):
        response = self.client.get(reverse('category-detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "New Category 1")
    
    
    # Test for modifying a category by anonymous, non-staff and staff user
    def test_patch_category(self):
        data = {
            "name": "Partially Updated Name",
        }
        
        # Anonymous User
        response = self.client.patch(reverse('category-detail', args=[self.category1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Non-staff user
        self.client.login(username='non_staff_user', email="non_staff_user@mail.com", password="nonstaffpass123")
        response = self.client.patch(reverse('category-detail', args=[self.category1.id]),  data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.category1.name, 'New Category 1')
        self.assertEqual(self.category1.slug, 'new-category-1')
        self.client.logout()

        # Staff User
        self.client.login(username='staff_user', email="staff_user@mail.com", password="staffpass123")
        response = self.client.patch(reverse('category-detail', args=[self.category1.id]),  data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)       
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, 'Partially Updated Name')
        self.assertEqual(self.category1.slug, 'new-category-1')
     
    
    # Test for deleting a category by anonymous, non-staff and staff user
    def test_delete_category(self):
        # Anonymous user
        response = self.client.delete(reverse('category-detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
     
        # Non-staff User
        self.client.login(username='non_staff_user', email="non_staff_user@mail.com", password="nonstaffpass123")
        response = self.client.delete(reverse('category-detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Staff user
        self.client.login(username='staff_user', email='staff_user@mail.com', password='staffpass123')
        response = self.client.delete(reverse('category-detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # verifying that category1 is deleted  
        response = self.client.get(reverse('category-detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
           


# Tests for Product APIs
# -----------------------
class ProductAPITests(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.staff_user = get_user_model().objects.create_user(
            username='staff_user', 
            email='staff_user@mail.com',
            password='staffpass123',
            is_staff = True,
        )
        cls.non_staff_user = get_user_model().objects.create_user(
            username='non_staff_user', 
            email='non_staff_user@mail.com',
            password='nonstaffpass123',
            is_staff=False
        )
        cls.category1 = Category.objects.create(name="New Category 1")
        cls.category2 = Category.objects.create(name="New Category 2")
        cls.product1 = Product.objects.create(
            name = 'First Product',
            description = 'First Description',
            price = 255.55,
            category = cls.category1,
        )
        cls.product2 = Product.objects.create(
            name = 'Second Product',
            description = 'Second Description',
            price = 100,
            category = cls.category2,
        )
        
        
    # Test for getting product-list - any user
    def test_get_product_list(self):
        response = self.client.get(reverse('product-list'))
        # print('product list get ok')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)      
    
        
    # Test for posting a product to the product list - anonymous, non-staff, staff user
    def test_post_product(self):
        new_product_data  = {
            "name": "New Product",
            "description": "New Product Description",
            "price": 500,
            "category": self.category1.id
        }
        # Anonymous user
        response = self.client.post(reverse('product-list'), new_product_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Non-staff user
        self.client.login(username='non_staff_user', email="non_staff_user@mail.com", password="nonstaffpass123")
        response = self.client.post(reverse('product-list'), new_product_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
        # Staff user
        self.client.login(username='staff_user', email="staff_user@mail.com", password="staffpass123")
        response = self.client.post(reverse('product-list'), new_product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        most_recent_product = Product.objects.order_by('-created_at').first()
        self.assertEqual(most_recent_product.name, 'New Product')
    
    
    # Test for getting single product using product id - any user
    def test_get_product_by_id(self):
        response = self.client.get(reverse('product-detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "First Product")
        # print('Test done get single product')
    
    
    # Test for modifying a product - anonymous, non-staff, staff user
    def test_patch_product(self):
        data = {
            "name": "Updated Name",
            "price": 800,
        }
        
        # Anonymous User
        response = self.client.patch(reverse('product-detail', args=[self.product1.id]), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print('test ok for patch product - anonymous user')
        
        # Non-staff user
        self.client.login(username='non_staff_user', email="non_staff_user@mail.com", password="nonstaffpass123")
        response = self.client.patch(reverse('product-detail', args=[self.product1.id]),  data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.product1.name, 'Updated Name')
        self.client.logout()
        print("test ok for non-staff product updating")

        # Staff User
        self.client.login(username='staff_user', email="staff_user@mail.com", password="staffpass123")
        response = self.client.patch(reverse('product-detail', args=[self.product1.id]),  data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)       
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.name, 'Updated Name')
        self.assertEqual(self.product1.price, 800)
        print('test is ok for updating product by staff user')
     
    
    
    # Test for deleting a product - anonymous, non-staff, staff user
    def test_delete_product(self):
        # Anonymous user
        response = self.client.delete(reverse('product-detail', args=[self.category1.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        print('test ok for deleting product by unauthorized user')
     
        # Non-staff User
        self.client.login(username='non_staff_user', email="non_staff_user@mail.com", password="nonstaffpass123")
        response = self.client.delete(reverse('product-detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print('test ok for deleting product by authorized but non-staff user')

        
        # Staff user
        self.client.login(username='staff_user', email='staff_user@mail.com', password='staffpass123')
        response = self.client.delete(reverse('product-detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # verifying that product1 is deleted  
        response = self.client.get(reverse('product-detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.client.logout()
        print('test ok for deleting product by staff user')
