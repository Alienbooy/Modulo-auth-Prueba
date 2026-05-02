"""
Router CQRS — dirige operaciones de base de datos al servidor correcto.

Principio: los modelos de escritura van a write_db,
los modelos de lectura van a read_db.
Nunca se permiten relaciones cruzadas entre bases de datos.
"""

# Modelos que pertenecen a write_db
WRITE_MODELS = {"user", "event"}

# Modelos que pertenecen a read_db
READ_MODELS = {"userview"}

# Nombre de la app propietaria de estos modelos
APP_LABEL = "users"


class CQRSRouter:
    """
    Router de base de datos que implementa separación CQRS.

    - User, Event → write_db  (operaciones de escritura y sus lecturas)
    - UserView     → read_db  (proyección de solo lectura)

    No se permiten relaciones entre bases de datos (allow_relation → False
    para modelos en distintas bases de datos).
    """

    def db_for_read(self, model, **hints):
        """Determina qué DB usar para operaciones SELECT."""
        if model._meta.app_label == APP_LABEL:
            model_name = model._meta.model_name
            if model_name in READ_MODELS:
                return "read_db"
            if model_name in WRITE_MODELS:
                return "write_db"
        return None

    def db_for_write(self, model, **hints):
        """Determina qué DB usar para operaciones INSERT/UPDATE/DELETE."""
        if model._meta.app_label == APP_LABEL:
            model_name = model._meta.model_name
            if model_name in READ_MODELS:
                return "read_db"
            if model_name in WRITE_MODELS:
                return "write_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Permite relaciones solo entre modelos de la misma base de datos.
        Previene FK cruzadas que romperían la separación CQRS.
        """
        db_set = {
            self.db_for_write(type(obj1)),
            self.db_for_write(type(obj2)),
        }
        # Si ambos están en la misma DB (un único elemento en el set), OK
        if len(db_set) == 1:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Controla dónde se crean las tablas durante las migraciones.
        - write_db: User, Event
        - read_db:  UserView
        """
        if app_label != APP_LABEL:
            return None

        if model_name is None:
            return None

        model_name_lower = model_name.lower()

        if db == "write_db":
            return model_name_lower in WRITE_MODELS
        if db == "read_db":
            return model_name_lower in READ_MODELS

        return None
