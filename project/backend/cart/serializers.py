from rest_framework import serializers
from cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class CartSerializer(serializers.HyperlinkedModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "customer",
            "items",
            "total_price",
        ]
        read_only_fields = ("customer", "total_price")
