from pathlib import Path
import os

# =========================
# Rutas base del proyecto
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# Seguridad / Debug
# =========================
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key-CHANGE-ME")
DEBUG = True  # Cambia a False en producción
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if os.environ.get("DJANGO_ALLOWED_HOSTS") else []

# =========================
# Apps instaladas
# =========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # App local
    "journal",
]

# =========================
# Middleware
# =========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# =========================
# URLs / WSGI
# =========================
ROOT_URLCONF = "inner_light_ai.urls"
WSGI_APPLICATION = "inner_light_ai.wsgi.application"

# =========================
# Templates
# =========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # tus plantillas globales
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Para poder usar MEDIA_URL en templates si lo necesitas
                "django.template.context_processors.media",
            ],
        },
    },
]

# =========================
# Base de datos (SQLite)
# =========================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# =========================
# Internacionalización
# =========================
LANGUAGE_CODE = "es"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# =========================
# Archivos estáticos / media
# =========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    # Si tienes una carpeta de estáticos del proyecto (opcional):
    # BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================
# Autenticación / Login
# =========================
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/accounts/profile/"

# =========================
# Email (dev por defecto)
# =========================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "25"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "False").lower() == "true"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL", "False").lower() == "true"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "webmaster@localhost")

# =========================
# Mensajes (Flash)
# =========================
from django.contrib.messages import constants as messages
MESSAGE_STORAGE = "django.contrib.messages.storage.fallback.FallbackStorage"
# Puedes mapear niveles a clases CSS si lo deseas:
MESSAGE_TAGS = {
    messages.DEBUG: "debug",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "error",
}

# =========================
# DeepSeek (IA) - Config
# =========================
# Usa variables de entorno en producción:
# export DEEPSEEK_API_KEY="sk-...."
# export DEEPSEEK_MODEL="deepseek-chat"
# (puedes cambiar el modelo por el que tengas habilitado)
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# =========================
# (Opcional) Compatibilidad previa con OpenAI
# =========================
# Si tenías llaves previas de OpenAI en tu entorno, las dejamos definidas pero NO se usan
# en el flujo actual; ahora todo llama a DeepSeek desde journal/views.py
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_ORG = os.environ.get("OPENAI_ORG", "")

# =========================
# Seguridad adicional básica
# =========================
CSRF_TRUSTED_ORIGINS = [
    # Ejemplo: "https://tu-dominio.com"
    # Agrega aquí dominios de despliegue si usas HTTPS reverse proxy
]

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"
