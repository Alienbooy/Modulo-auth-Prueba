"""
Command Serializer — Responsabilidad única: validar datos de entrada del comando.

Principio de diseño:
- Solo valida y limpia datos de entrada (SRP).
- No ejecuta ninguna lógica de negocio.
- No accede a la base de datos excepto para validar unicidad.
"""

from rest_framework import serializers

from users.models.user import User


class CreateUserSerializer(serializers.Serializer):
    """
    Serializer de validación para el comando CreateUser.
    Valida formato, unicidad y requisitos mínimos de seguridad.
    """

    username = serializers.CharField(
        max_length=150,
        min_length=3,
        trim_whitespace=True,
    )
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8,
        write_only=True,  # El password nunca se incluye en la respuesta
        style={"input_type": "password"},
    )

    def validate_username(self, value: str) -> str:
        """Verifica que el username no esté en uso en write_db."""
        if User.objects.using("write_db").filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate_email(self, value: str) -> str:
        """Verifica que el email no esté en uso en write_db."""
        if User.objects.using("write_db").filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está registrado.")
        return value
