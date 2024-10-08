"""
Django settings for lms project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from pathlib import Path
from corsheaders.defaults import default_headers
from datetime import timedelta
from decouple import config
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!!
DEBUG = config('DEBUG', cast=bool)

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    #Third-party Apps
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'core.celery.CeleryConfig',

    #Local Apps
    'user',
    'transaction',
    #'authMixin',
]

#USER MODEL
AUTH_USER_MODEL = "user.User"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "core.middleware.CaptureExceptionMiddleware",
]

AUTHENTICATION_BACKENDS = [
    'user.backends.CustomAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = "static/"
STATIC_ROOT = "static/"

WSGI_APPLICATION = 'core.wsgi.application'
WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = ["https://*.ridwanray.com"]
LOGIN_URL = "rest_framework:login"
LOGOUT_URL = "rest_framework:logout"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    "default": dj_database_url.config(default=config('DATABASE_URL'))
}



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "core.pagination.CustomPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id"
    
}
# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
TIME_ZONE = "Africa/Lagos"
DATE_INPUT_FORMATS = [
    "%d/%m/%Y",
    "%d/%m/%y",  # '10/02/2020', '10/02/20'
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%m/%d/%y",  # '2006-10-25', '10/25/2006', '10/25/06'
    "%b %d %Y",
    "%b %d, %Y",  # 'Oct 25 2006', 'Oct 25, 2006'
    "%d %b %Y",
    "%d %b, %Y",  # '25 Oct 2006', '25 Oct, 2006'
    "%B %d %Y",
    "%B %d, %Y",  # 'October 25 2006', 'October 25, 2006'
    "%d %B %Y",
    "%d %B, %Y",  # '25 October 2006', '25 October, 2006'
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

TOKEN_LIFESPAN = 24 #hrs


CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_BROKER_URL = config('RABBITMQ_URL')
FLOWER_BASIC_AUTH = os.environ.get('FLOWER_BASIC_AUTH')
EMAIL_FROM = config("SENDER_EMAIL")

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}

SPECTACULAR_SETTINGS = {
    'SCHEMA_PATH_PREFIX': r'/api/v1',
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.generators.SchemaGenerator',
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'COMPONENT_SPLIT_PATCH': True,
    'COMPONENT_SPLIT_REQUEST': True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
        "displayRequestDuration": True
    },
    'UPLOADED_FILES_USE_URL': True,
    'TITLE': 'Microservice Authentication Service',
    'DESCRIPTION': 'Microservice Authentication Service',
    'VERSION': '0.2.0',
    'LICENCE': {'name': 'BSD License'},
    'CONTACT': {'name': 'Ridwanray', 'email': 'alabarise@gmail.com'},
    #OAUTH2 SPEC
    'OAUTH2_FLOWS': [],
    'OAUTH2_AUTHORIZATION_URL': None,
    'OAUTH2_TOKEN_URL': None,
    'OAUTH2_REFRESH_URL': None,
    'OAUTH2_SCOPES': None,
}

MAX_LOGIN_ATTEMPT = config('MAX_LOGIN_ATTEMPT', cast=int)
