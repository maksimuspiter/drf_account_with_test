from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "description"]


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField(source="get_image_url", read_only=True)
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "short_description",
            "price_now",
            "quantity",
            "category",
            "image_url",
            "image",
        ]
