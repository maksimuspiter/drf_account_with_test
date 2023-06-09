from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "users"

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
]
