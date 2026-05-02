"""
ProjectorService — Responsabilidad única: sincronizar User → UserView.

Principio de diseño:
- Escucha eventos y proyecta datos al modelo de lectura (read_db).
- No conoce nada sobre reglas de negocio ni validaciones.
- SRP: solo transforma y persiste la proyección.
"""

from users.models.user import User
from users.models.user_view import UserView


class ProjectorService:
    """
    Servicio que crea o actualiza proyecciones en read_db
    a partir de los modelos de escritura.
    """

    @staticmethod
    def project_user(user: User) -> UserView:
        """
        Crea o actualiza el UserView correspondiente en read_db.

        Solo proyecta campos públicos: id, username, email, created_at.
        El campo password nunca se proyecta al read model.

        Args:
            user: Instancia del modelo de escritura User.

        Returns:
            La instancia de UserView creada o actualizada.
        """
        user_view, _ = UserView.objects.using("read_db").update_or_create(
            id=user.id,
            defaults={
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at,
            },
        )
        return user_view
