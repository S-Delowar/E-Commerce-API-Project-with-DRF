from django.test import TestCase
from shop.models import Category, Product, ProductImage
from uuid import UUID
from django.core.files.uploadedfile import SimpleUploadedFile


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
        print(f"image name - {self.product_image.image.name}")
        self.assertEqual(self.product_image.product, self.product)
        self.assertTrue(self.product_image.image.name.startswith("product_images/test_image")) 
    
    def test_image_str(self):
        self.assertEqual(str(self.product_image), 'Image for Test Product')