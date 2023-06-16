from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-users/", include("users.urls", namespace="users")),
    path("api-movie/", include("movie.urls", namespace="movie")),
    path("api-auth/", include("rest_framework.urls")),
]
