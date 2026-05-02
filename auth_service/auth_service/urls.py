"""URLs raíz del proyecto auth_service."""

from django.urls import include, path

urlpatterns = [
    path("api/users/", include("users.urls", namespace="users")),
]
