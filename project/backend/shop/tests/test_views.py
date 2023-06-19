from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from shop.models import Product, Category

# from django.db import transaction


class ProductAndCategoryTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="test_user", password="secret")
        User.objects.create_superuser(username="test_admin", password="secret")
        cat = Category.objects.create(
            title="Test Category Title",
            description="Test Category Description",
        )
        Product.objects.create(
            title="Test Product Title",
            description="Test Product Description",
            short_description="Test Product Short Description",
            price_now=1000,
            quantity=10,
            category=cat,
        )

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client.logout()

    def test_product_list(self):
        response = self.client.get("/shop/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_category_list(self):
        response = self.client.get("/shop/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_category_create(self):
        data = {
            "title": "Test Category1",
        }
        response = self.client.post("/shop/categories/", data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login(username="test_user", password="secret")
        response = self.client.post("/shop/categories/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test_admin", password="secret")
        response = self.client.post("/shop/categories/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.last().title, "Test Category1")

    def test_product_create(self):
        category = Category.objects.first()
        data = {"title": "Test Product1", "category": category.id}
        response = self.client.post("/shop/products/", data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.login(username="test_user", password="secret")
        response = self.client.post("/shop/products/", data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username="test_admin", password="secret")
        response = self.client.post("/shop/products/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.last().title, "Test Product1")
        self.assertEqual(Product.objects.last().category, category)
