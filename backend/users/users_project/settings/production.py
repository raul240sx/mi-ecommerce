import os
from .base import *
from django.core.exceptions import ImproperlyConfigured

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False

if not SECRET_KEY:
    raise ImproperlyConfigured("La variable SECRET_KEY no está configurada.")

ALLOWED_HOSTS = [os.getenv('DOMAIN_NAME'), 'users-service']

CSRF_TRUSTED_ORIGINS = [f"https://{os.getenv('DOMAIN_NAME')}"]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False 

STATIC_URL = '/static/users/'
STATIC_ROOT = '/usr/src/app/staticfiles'

MEDIA_URL = '/media/users/'
MEDIA_ROOT = '/usr/src/app/media'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        "rest_framework.permissions.IsAuthenticated",
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Users API',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    'SWAGGER_UI_FAVICON_HREF': '/static/users/favicon.ico',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT', 5432),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
SITE_URL = 'http://192.168.1.201:3000'
SITE_NAME = 'Guitar Zone'
VERIFY_URL_PATH = 'auth/verify-email'
RESET_URL_PATH = 'auth/password-reset-confirm'