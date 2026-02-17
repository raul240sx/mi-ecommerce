from .base import *
from django.core.exceptions import ImproperlyConfigured


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False

if not SECRET_KEY:
    raise ImproperlyConfigured("La variable SECRET_KEY no está configurada en el entorno de producción.")


ALLOWED_HOSTS = [os.getenv('DOMAIN_NAME'), 'products-service']
CSRF_TRUSTED_ORIGINS = [f"https://{os.getenv('DOMAIN_NAME')}"]

# BLOQUE DE SEGURIDAD 
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.base.custom_authentication.CustomAuthentication',
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}





# Database
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


# Static files 

# Cambia esto:
STATIC_URL = '/static/products/'
STATIC_ROOT = '/usr/src/app/staticfiles'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Documentacion de Products-API',
    'DESCRIPTION': 'Documentación pública de API de e-commerce',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_FAVICON_HREF': '/static/users/favicon.ico',
    'COMPONENT_SPLIT_PATCH': True,
    'SECURITY': [{'BearerAuth': []}],
    'APPEND_COMPONENTS': {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
}