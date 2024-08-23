"""
Django settings for rn24 project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url
import factory
import sentry_sdk

factory.Faker._DEFAULT_LOCALE = "it_IT"


def bool_from_env(key):
    var = os.getenv(key)
    if not var:
        return None
    if var.upper() in ("Y", "TRUE", "ON", "1"):
        return True
    return False


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool_from_env("DJANGO_DEBUG")

SILK_ENABLED = bool_from_env("SILK_ENABLED")

ALLOWED_HOSTS = [
    os.getenv("ALLOWED_HOST"),
]

USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = ["https://" + os.getenv("ALLOWED_HOST", "")]

# Application definition

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django_extensions",
    "django_linear_migrations",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_gis",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "import_export",
    "fontawesomefree",
    "authentication.apps.AuthenticationConfig",
    "people.apps.PeopleConfig",
    "events.apps.EventsConfig",
    "maps.apps.MapsConfig",
    "api.apps.ApiConfig",
    "cms.apps.CmsConfig",
    "settings.apps.SettingsConfig",
    "django.contrib.admin",
    "colorfield",
]

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

if SILK_ENABLED:
    INSTALLED_APPS.append("silk")
    MIDDLEWARE.append("silk.middleware.SilkyMiddleware")

    SILKY_AUTHENTICATION = True
    SILKY_AUTHORISATION = True
    SILKY_META = True
    SILKY_PYTHON_PROFILER = True
    SILKY_PYTHON_PROFILER_BINARY = True


ROOT_URLCONF = "rn24.urls"

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

WSGI_APPLICATION = "rn24.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    ),
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "it-IT"

TIME_ZONE = "Europe/Rome"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/api/static/"
MEDIA_URL = "/api/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "MEDIA")
STATIC_ROOT = os.path.join(BASE_DIR, "STATIC")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AUTH_USER_MODEL = "authentication.User"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "RN24 backend",
    "DESCRIPTION": "RN24 backend API documentation",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAuthenticated"],
}

WAGTAIL_SITE_NAME = "RN24 backoffice CMS"
WAGTAILADMIN_BASE_URL = "/cms"

# TODO: enable this with an env variable only for test environment
CORS_ALLOW_ALL_ORIGINS = True

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "authentication.backends.AGESCIAuthenticationBackend",
]

AGESCI_HOSTNAME = os.getenv("AGESCI_HOSTNAME")
AGESCI_SECRET = os.getenv("AGESCI_SECRET")
AGESCI_KEY = os.getenv("AGESCI_KEY")

PRIVATE_KEY_PATH = "privkey.pem"
PUBLIC_KEY_PATH = "pubkey.pem"
PUBLIC_KEY = open(PUBLIC_KEY_PATH).read() if os.path.exists(PUBLIC_KEY_PATH) else None


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        # "level": "DEBUG" if DEBUG else "INFO",
        "level": "INFO",
    },
}

RN24_FRONTEND_URL = os.getenv("RN24_FRONTEND_URL", "")

SENTRY_DSN = os.getenv("SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

SHELL_PLUS_PRINT_SQL_TRUNCATE = None

if DEBUG:
    CACHE_TIMEOUT = 1
else:
    CACHE_TIMEOUT = 60 * 1  # seconds

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
        "TIMEOUT": CACHE_TIMEOUT,
    }
}

IMPORT_EXPORT_EXPORT_PERMISSION_CODE = "change"

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = bool_from_env("EMAIL_USE_TLS")
EMAIL_USE_SSL = bool_from_env("EMAIL_USE_SSL")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000
