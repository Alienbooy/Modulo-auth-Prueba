"""
Query Handler — Responsabilidad única: recuperar un UserView del read model.

Principio de diseño:
- Accede exclusivamente a read_db. Nunca toca write_db.
- No lanza excepciones de ORM hacia la capa de presentación.
  Retorna None si el recurso no existe — la view decide la respuesta HTTP.
- Método estático: no requiere estado, máxima simplicidad (SRP).
"""

import uuid
from typing import Optional

from users.models.user_view import UserView


class GetUserHandler:
    """
    Handler de la consulta GetUser.
    Lee exclusivamente del read model en read_db.
    Retorna None si el usuario no existe (no propaga ORM exceptions).
    """

    @staticmethod
    def handle(user_id: uuid.UUID) -> Optional[UserView]:
        """
        Recupera un UserView por su UUID desde read_db.

        Args:
            user_id: UUID del usuario a consultar.

        Returns:
            La instancia de UserView si existe, None en caso contrario.
        """
        return (
            UserView.objects
            .using("read_db")
            .filter(id=user_id)
            .first()
        )
