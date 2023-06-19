from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "shop"

router = routers.DefaultRouter()
router.register(r"products", views.ProductViewSet, basename="products")
router.register(r"categories", views.CategoryViewSet, basename="categories")

urlpatterns = [
    path("", include(router.urls)),
]
