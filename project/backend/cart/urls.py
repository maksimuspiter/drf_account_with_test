from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "cart"

router = routers.DefaultRouter()
router.register(r"cart", views.CartViewSet, basename="cart")
router.register(r"cart_items", views.CartItemViewSet, basename="cart_items")

urlpatterns = [
    path("", include(router.urls)),
]
