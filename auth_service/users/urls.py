"""URLs de la app users."""

from django.urls import path

from users.views import GetUserView, RegisterView

app_name = "users"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("<uuid:pk>/", GetUserView.as_view(), name="get-user"),
]
