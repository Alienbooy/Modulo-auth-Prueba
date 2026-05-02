"""
Command Handler — Responsabilidad única: procesar el comando CreateUser.

Principio de diseño:
- Recibe datos ya validados del serializer.
- Delega la lógica de negocio completa al UserWriterService.
- No contiene lógica de persistencia ni validación.
- Retorna una respuesta estructurada al presentador (view).
"""

from users.models.user import User
from users.services.user_writer import UserWriterService


class CreateUserHandler:
    """
    Handler del comando de creación de usuario.
    Actúa como puente entre la capa de presentación y los servicios.
    """

    def __init__(self, writer_service: UserWriterService = None):
        # Inyección de dependencias (SOLID: DIP)
        self._writer = writer_service or UserWriterService()

    def handle(self, validated_data: dict) -> User:
        """
        Ejecuta el comando CreateUser.

        Args:
            validated_data: Diccionario limpio proveniente del serializer.
                            Debe contener: username, email, password.

        Returns:
            La instancia de User recién creada en write_db.
        """
        return self._writer.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            raw_password=validated_data["password"],
        )
