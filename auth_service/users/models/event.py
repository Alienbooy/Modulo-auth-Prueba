"""
Event Store — vive en write_db.

Responsabilidad única: persistir eventos de dominio de forma inmutable.
Cada evento representa algo que ocurrió en el sistema (past tense).
"""

import uuid

from django.db import models


class EventType(models.TextChoices):
    USER_CREATED = "USER_CREATED", "User Created"


class Event(models.Model):
    """
    Registro inmutable de un evento de dominio.
    Nunca se actualiza ni elimina — solo se inserta (append-only).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=100, choices=EventType.choices)
    aggregate_id = models.UUIDField(help_text="ID de la entidad que originó el evento")
    payload = models.JSONField(help_text="Datos del evento en formato JSON")
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "users"
        db_table = "users_event"
        ordering = ["occurred_at"]

    def __str__(self) -> str:
        return f"{self.event_type} [{self.aggregate_id}] @ {self.occurred_at}"
