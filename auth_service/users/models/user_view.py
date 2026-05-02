"""
Modelo de LECTURA — vive exclusivamente en read_db.

Responsabilidad única: proyección de datos públicos del usuario
sin información sensible. Se sincroniza desde write_db via projector.
"""

import uuid

from django.db import models


class UserView(models.Model):
    """
    Modelo de lectura (Read Model / Projection).
    No contiene password ni datos sensibles.
    Almacenado en read_db. Solo se lee, nunca se escribe directamente.
    """

    id = models.UUIDField(primary_key=True, editable=False)
    username = models.CharField(max_length=150)
    email = models.EmailField()
    created_at = models.DateTimeField()

    class Meta:
        app_label = "users"
        db_table = "users_userview"
        managed = True  # Django gestiona la tabla en read_db vía migraciones

    def __str__(self) -> str:
        return self.username
