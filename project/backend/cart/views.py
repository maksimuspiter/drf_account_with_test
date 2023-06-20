from rest_framework import viewsets
from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer
from cart.permissions import IsAdminOrOwner, IsAdminOrCreateOnly

# from rest_framework.permissions import IsAuthenticated


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAdminOrOwner]


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAdminOrCreateOnly]

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(customer=self.request.user.account)
        product = serializer.validated_data.get("product")

        for item in cart.items.all():
            if item.product == product:
                quantity = serializer.validated_data.get("quantity", 1)

                item.quantity += quantity
                item.save()
                break
        else:
            new_cart_item = serializer.save()
            cart.items.add(new_cart_item)
            cart.save()
