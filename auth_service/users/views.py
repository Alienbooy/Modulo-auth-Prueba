"""
Views — Solo orquesta. Sin lógica de negocio.

Reglas CQRS aplicadas:
- Views = presentadores puros: HTTP in → handler → HTTP out.
- No acceden a modelos directamente.
- No construyen estructuras de datos manualmente (delegan al serializer).
- Manejo de errores mínimo y consistente.
"""

import uuid

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from users.command.handlers import CreateUserHandler
from users.command.serializers import CreateUserSerializer
from users.query.handlers import GetUserHandler
from users.query.serializers import UserViewSerializer


class RegisterView(APIView):
    """
    POST /api/users/register/

    Flujo estricto:
      1. Validar entrada con CreateUserSerializer (command side).
      2. Ejecutar CreateUserHandler (delega toda la lógica).
      3. Responder con RegisterResponseSerializer (query side read model).
    """

    def post(self, request: Request) -> Response:
        # Paso 1 — Validar datos de entrada (command serializer)
        input_serializer = CreateUserSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(
                input_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Paso 2 — Ejecutar comando; toda la lógica vive en el handler
        user = CreateUserHandler().handle(input_serializer.validated_data)

        # Paso 3 — Serializar respuesta usando el mismo serializer de query
        # (DRY: no duplicamos la estructura del response manualmente)
        output_serializer = RegisterResponseSerializer(user)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


class GetUserView(APIView):
    """
    GET /api/users/<uuid:pk>/

    Consulta exclusivamente el read model (read_db).
    La view nunca importa ni conoce UserView directamente.
    """

    def get(self, request: Request, pk: uuid.UUID) -> Response:
        # Paso 1 — Ejecutar query; toda la lógica vive en el handler
        user_view = GetUserHandler.handle(pk)

        if user_view is None:
            return Response(
                {"detail": "Usuario no encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Paso 2 — Serializar y retornar read model
        serializer = UserViewSerializer(user_view)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# Serializer de respuesta inline — solo para el registro
# Evita duplicar la estructura dict manual que viola DRY
# ---------------------------------------------------------------------------
from rest_framework import serializers
from users.models.user import User


class RegisterResponseSerializer(serializers.ModelSerializer):
    """
    Serializer de respuesta para el comando de registro.
    Expone únicamente datos públicos del write model recién creado.
    """

    class Meta:
        model = User
        fields = ["id", "username", "email"]
        read_only_fields = fields
