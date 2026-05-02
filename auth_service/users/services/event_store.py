"""
EventStoreService — Responsabilidad única: persistir eventos de dominio.

Principio de diseño:
- Append-only: los eventos no se modifican ni eliminan.
- Desacoplado: no conoce nada sobre User ni UserView.
- SRP: su única responsabilidad es guardar eventos.
"""

from users.models.event import Event, EventType


class EventStoreService:
    """
    Servicio que persiste eventos de dominio en el event store (write_db).
    Completamente desacoplado de la lógica de negocio.
    """

    @staticmethod
    def record(
        event_type: EventType,
        aggregate_id,
        payload: dict,
    ) -> Event:
        """
        Persiste un evento de dominio de forma inmutable en write_db.

        Args:
            event_type:    Tipo de evento (ej: EventType.USER_CREATED)
            aggregate_id:  UUID de la entidad que generó el evento
            payload:       Diccionario con datos relevantes del evento

        Returns:
            La instancia del evento persistido.
        """
        return Event.objects.using("write_db").create(
            event_type=event_type,
            aggregate_id=aggregate_id,
            payload=payload,
        )
