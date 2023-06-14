from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "users"

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet, basename="users")
router.register(r"accounts", views.AccountForAdminViewSet, basename="accounts")
router.register(r"portfolio", views.AccountViewSet, basename="portfolios")

urlpatterns = [
    path("", include(router.urls)),
]
