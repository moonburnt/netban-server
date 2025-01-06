from pathlib import Path
from .utils import EnvLoader

env = EnvLoader()
env.load()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env.get_str("DJANGO_SECRET_KEY")
DEBUG = env.get_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = env.get_list("DJANGO_ALLOWED_HOSTS")

AUTH_USER_MODEL = "users.User"

# Netban server settings
API_VERSION = "0.1.0"
HEADLESS_MODE = env.get_bool("HEADLESS_MODE", False)

# Application definition
if HEADLESS_MODE:
    INSTALLED_APPS = []
else:
    INSTALLED_APPS = [
        "django.contrib.admin",
    ]

INSTALLED_APPS.extend(
    [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        # DB
        "django.contrib.postgres",
        "psqlextra",
        # DRF
        "rest_framework",
        # Swagger
        "drf_spectacular",
        # Custom
        "server.users",
        "server.platform",
        "server.restrictions",
    ]
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "psqlextra.backend",
        "NAME": env.get_str("POSTGRES_DB"),
        "USER": env.get_str("POSTGRES_USER"),
        "PASSWORD": env.get_str("POSTGRES_PASSWORD"),
        "HOST": env.get_str("POSTGRES_HOST"),
        "PORT": env.get_int("POSTGRES_PORT"),
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# DRF
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPEND_SLASH = True
