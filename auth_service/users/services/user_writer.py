"""
UserWriterService — Orquesta la escritura completa del agregado User.

Responsabilidad: coordinar los tres pasos de la operación de escritura:
  1. Persistir el User en write_db
  2. Registrar el evento de dominio en el event store
  3. Proyectar la vista al read_db

Principio de diseño:
- Actúa como punto de entrada único para comandos de escritura.
- Delega cada sub-responsabilidad a su servicio correspondiente.
- No contiene lógica de validación (esa vive en los serializers).
"""

from users.models.event import EventType
from users.models.user import User
from users.services.event_store import EventStoreService
from users.services.projector import ProjectorService


class UserWriterService:
    """
    Orquestador de escritura para la entidad User.
    Coordina la persistencia en write_db, el event store y la proyección.
    """

    def __init__(
        self,
        event_store: EventStoreService = None,
        projector: ProjectorService = None,
    ):
        # Inyección de dependencias — permite testear con mocks (SOLID: DIP)
        self._event_store = event_store or EventStoreService()
        self._projector = projector or ProjectorService()

    def create_user(self, username: str, email: str, raw_password: str) -> User:
        """
        Crea un usuario aplicando el flujo completo CQRS + Event Sourcing:
          1. Persiste User en write_db con password hasheado.
          2. Registra evento USER_CREATED en el event store.
          3. Proyecta UserView en read_db.

        Args:
            username:     Nombre único de usuario.
            email:        Dirección de correo única.
            raw_password: Contraseña en texto plano (se hashea antes de guardar).

        Returns:
            La instancia de User recién creada.
        """
        # Paso 1: crear y persistir el usuario en write_db
        user = User(username=username, email=email)
        user.set_password(raw_password)
        user.save(using="write_db")

        # Paso 2: registrar evento de dominio (append-only)
        self._event_store.record(
            event_type=EventType.USER_CREATED,
            aggregate_id=user.id,
            payload={
                "username": user.username,
                "email": user.email,
                "occurred_at": user.created_at.isoformat(),
            },
        )

        # Paso 3: proyectar al read model
        self._projector.project_user(user)

        return user
