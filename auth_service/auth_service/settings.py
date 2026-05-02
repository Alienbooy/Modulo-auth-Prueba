"""
Django settings for auth_service project — CQRS + Event Sourcing.

Configuración con dos bases de datos PostgreSQL:
  - write_db: base de datos de escritura (User, Event)
  - read_db:  base de datos de lectura  (UserView)

Las credenciales se leen desde variables de entorno o un archivo .env
usando python-decouple (pip install python-decouple).
"""

from pathlib import Path

from decouple import Csv, config

# ---------------------------------------------------------------------------
# Rutas base
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Seguridad — nunca hardcodeada en producción
# ---------------------------------------------------------------------------
SECRET_KEY = config("SECRET_KEY", default="si-no-tiene-el-env-se-pone-este-por-defecto")


DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=Csv())

# ---------------------------------------------------------------------------
# Aplicaciones instaladas
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    # Local
    "users",
]

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

# ---------------------------------------------------------------------------
# URLs
# ---------------------------------------------------------------------------
ROOT_URLCONF = "auth_service.urls"

WSGI_APPLICATION = "auth_service.wsgi.application"

# ---------------------------------------------------------------------------
# Templates (mínimo necesario para DRF)
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# Bases de datos — CQRS: write_db (escritura) y read_db (lectura)
# ---------------------------------------------------------------------------
_DB_ENGINE = "django.db.backends.postgresql"
_DB_USER = config("DB_USER", default="postgres")
_DB_PASSWORD = config("DB_PASSWORD", default="postgres")
_DB_HOST = config("DB_HOST", default="localhost")
_DB_PORT = config("DB_PORT", default="5432")

DATABASES = {
    # Base de datos de ESCRITURA — almacena User y Event
    "write_db": {
        "ENGINE": _DB_ENGINE,
        "NAME": config("WRITE_DB_NAME", default="auth_write_db"),
        "USER": _DB_USER,
        "PASSWORD": _DB_PASSWORD,
        "HOST": _DB_HOST,
        "PORT": _DB_PORT,
        "ATOMIC_REQUESTS": True,  # Garantiza atomicidad en cada request de escritura
    },
    # Base de datos de LECTURA — solo almacena UserView (proyección)
    "read_db": {
        "ENGINE": _DB_ENGINE,
        "NAME": config("READ_DB_NAME", default="auth_read_db"),
        "USER": _DB_USER,
        "PASSWORD": _DB_PASSWORD,
        "HOST": _DB_HOST,
        "PORT": _DB_PORT,
        "ATOMIC_REQUESTS": False,  # Solo lecturas; sin transacciones innecesarias
    },
    # default = alias de write_db para satisfacer apps internas de Django
    "default": {
        "ENGINE": _DB_ENGINE,
        "NAME": config("WRITE_DB_NAME", default="auth_write_db"),
        "USER": _DB_USER,
        "PASSWORD": _DB_PASSWORD,
        "HOST": _DB_HOST,
        "PORT": _DB_PORT,
    },
}

# ---------------------------------------------------------------------------
# Router CQRS — dirige cada modelo a su base de datos correcta
# ---------------------------------------------------------------------------
DATABASE_ROUTERS = ["users.db_router.router.CQRSRouter"]

# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}

# ---------------------------------------------------------------------------
# Internacionalización
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "es-mx"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Archivos estáticos
# ---------------------------------------------------------------------------
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
