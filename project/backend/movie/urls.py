from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "movie"

router = routers.DefaultRouter()
router.register(r"movie", views.MovieViewSet, basename="movie")
router.register(r"resurse", views.ResourceViewSet, basename="resurse")


urlpatterns = [
    path("", include(router.urls)),
]
