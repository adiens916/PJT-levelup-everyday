"""
Django settings for levelup_everyday project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

backend_host = os.environ.get("BACKEND_HOST")
backend_domain = os.environ.get("BACKEND_WITH_DOMAIN")
frontend_port = os.environ.get("FRONTEND_PORT")
frontend_domain = os.environ.get("FRONTEND_WITH_DOMAIN")

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
]
ALLOWED_HOSTS.append(backend_host) if backend_host else None

# Access-Control-Allow-Origin 헤더에 주소를 자동으로 추가해줌
CORS_ALLOWED_ORIGINS = [
    f"http://localhost:{frontend_port}",
    f"http://127.0.0.1:{frontend_port}",
]
CORS_ALLOWED_ORIGINS.append(frontend_domain) if frontend_domain else None

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    # for frontend
    f"http://localhost:{frontend_port}",
    f"http://127.0.0.1:{frontend_port}",
]
CSRF_TRUSTED_ORIGINS.append(frontend_domain) if frontend_domain else None
# for admin page on the web server (not needed on localhost)
CSRF_TRUSTED_ORIGINS.append(backend_domain) if backend_domain else None

# Cache
# https://docs.djangoproject.com/en/4.1/topics/cache/#the-per-site-cache
CACHE_MIDDLEWARE_SECONDS = 0


# Application definition

INSTALLED_APPS = [
    # App
    "account",
    "habits",
    # Third-party
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    # Built-in
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "levelup_everyday.urls"

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

WSGI_APPLICATION = "levelup_everyday.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

AUTH_USER_MODEL = "account.User"

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DJANGO_DB_ENGINE"),
        "NAME": os.environ.get("DJANGO_DB_NAME"),
        "USER": os.environ.get("DJANGO_DB_USER"),
        "PASSWORD": os.environ.get("DJANGO_DB_PASSWORD"),
        "HOST": os.environ.get("DJANGO_DB_HOST"),
        "PORT": os.environ.get("DJANGO_DB_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "api/static/"
STATIC_ROOT = BASE_DIR / ".collected_static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
