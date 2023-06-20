from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-users/", include("users.urls", namespace="users")),
    path("api-auth/", include("rest_framework.urls")),
    path("shop/", include("shop.urls", namespace="shop")),
    path("cart/", include("cart.urls", namespace="cart")),
]
