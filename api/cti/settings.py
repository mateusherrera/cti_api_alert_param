"""
Settings para o projeto CTI.

:created by:    Mateus Herrera
:created at:    2024-10-25
"""

from os import path
from pathlib import Path
from decouple import config
from datetime import timedelta


# Configurações do projeto
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY')

if config('ENV') == 'prod':
    DEBUG = False
elif config('ENV') == 'dev':
    DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')
if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
elif not DEBUG:
    CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', default='').split(',')

# Definições de aplicativos e middlewares
INSTALLED_APPS = [
    # Apps padrão
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps de terceiros
    'decouple',
    'corsheaders',
    'django_filters',
    'rest_framework',

    # Apps internos
    'alert_param',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'cti.urls'

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
WSGI_APPLICATION = 'cti.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PSWD'),

        'OPTIONS': {
            'options': '-c search_path=django'
        },
    }
}

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

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/api/static/'
STATIC_ROOT = path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/api/media/'
MEDIA_ROOT = path.join(BASE_DIR, 'mediafiles')

# Rest Framework
REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
    ),

    # Permissions
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),

    # Throttling
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'user': '50/second',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
