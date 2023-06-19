from django.test import TestCase
from shop.models import Product, Category


class CreateProductAndCategoryTest(TestCase):
    def test_create_product_and_category(self):
        cat = Category.objects.create(
            title="Test Category Title",
            description="Test Category Description",
        )
        product = Product.objects.create(
            title="Test Product Title",
            description="Test Product Description",
            short_description="Test Product Short Description",
            price_now=1000,
            quantity=10,
            category=cat,
        )
        self.assertEqual(Product.objects.last().id, product.id)
        self.assertEqual(Category.objects.last().id, cat.id)

        self.assertEqual(product.title, "Test Product Title")
        self.assertEqual(product.category.title, cat.title)

    def test_create_product_and_category_with_blank(self):
        product = Product.objects.create(
            title="Test1",
        )
        self.assertEqual(Product.objects.last().id, product.id)
        self.assertEqual(product.category, None)
        self.assertEqual(product.description, "")
        self.assertEqual(product.quantity, 0)
        self.assertEqual(product.price_now, 0)
        self.assertEqual(product.short_description, "")
        self.assertFalse(product.image)
        self.assertEqual(
            product.get_image_url(),
            "http://127.0.0.1:8000/static/images/base_product.webp",
        )

        cat = Category.objects.create(
            title="Test Category Title",
        )
        self.assertEqual(Category.objects.last().id, cat.id)
        self.assertEqual(cat.description, "")
