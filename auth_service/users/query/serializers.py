"""
Query Serializer — Responsabilidad única: serializar el UserView para la respuesta.

Principio de diseño:
- Solo serializa datos del read model (SRP).
- No expone información sensible (sin password).
- Basado en ModelSerializer para máxima consistencia con el modelo.
"""

from rest_framework import serializers

from users.models.user_view import UserView


class UserViewSerializer(serializers.ModelSerializer):
    """
    Serializer de salida para el read model UserView.
    Nunca incluye password ni datos sensibles.
    """

    class Meta:
        model = UserView
        fields = ["id", "username", "email", "created_at"]
        read_only_fields = fields  # El read model es inmutable desde la API
