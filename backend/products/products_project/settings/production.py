from .base import *
from django.core.exceptions import ImproperlyConfigured


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False

if not SECRET_KEY:
    raise ImproperlyConfigured("La variable SECRET_KEY no está configurada en el entorno de producción.")


ALLOWED_HOSTS = [os.getenv('DOMAIN_NAME'), 'products-service']



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.base.custom_authentication.CustomAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 12,

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
        'securitySchemes': {
            'BearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT',
            }
        }
    },
}


# --- SEGURIDAD Y CORS PARA COOKIES ---
SECURE_SSL_REDIRECT = False
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'https://guitarzone.cl',
    'https://api.guitarzone.cl',
]

CSRF_TRUSTED_ORIGINS = [
    f'https://{os.getenv('DOMAIN_NAME')}',
    'http://localhost:5173'
]

# Dominios de Cookies 
SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None

# Atributos de seguridad
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'

CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_HTTPONLY = False 
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'

# Confianza en Cloudflare
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


DOMAIN_URL = f'https://{os.getenv('DOMAIN_NAME')}'