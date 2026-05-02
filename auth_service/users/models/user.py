"""
Modelo de ESCRITURA — vive exclusivamente en write_db.

Responsabilidad única: representar la entidad User con sus datos
sensibles (password hasheado) para operaciones de escritura.
"""

import uuid

from django.contrib.auth.hashers import make_password
from django.db import models


class User(models.Model):
    """
    Modelo de escritura.
    Almacenado en write_db. Nunca se expone directamente al cliente.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "users"
        db_table = "users_user"

    def set_password(self, raw_password: str) -> None:
        """Hashea y asigna el password"""
        self.password = make_password(raw_password)

    def __str__(self) -> str:
        return self.username
