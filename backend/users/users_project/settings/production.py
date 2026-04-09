import os
from .base import *
from django.core.exceptions import ImproperlyConfigured

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False

if not SECRET_KEY:
    raise ImproperlyConfigured("La variable SECRET_KEY no está configurada.")

ALLOWED_HOSTS = [os.getenv('DOMAIN_NAME'), 'users-service']



STATIC_URL = '/static/users/'
STATIC_ROOT = '/usr/src/app/staticfiles'

MEDIA_URL = '/media/users/'
MEDIA_ROOT = '/usr/src/app/media'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.users.auth.authentication.CookieJWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        "rest_framework.permissions.IsAuthenticated",
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'password_reset': '10/min',     ## cambiar a 5/min
        'register': '10/min',           ## cambiar a 2/min
    },

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
        ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,

    
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
SITE_URL = 'https://guitarzone.cl'
SITE_NAME = 'Guitar Zone'
VERIFY_URL_PATH = 'auth/verify-email'
RESET_URL_PATH = 'auth/password-reset-confirm'



# --- JWT CONFIG ---
INTERNAL_SERVICE_KEY = os.getenv('INTERNAL_SERVICE_KEY')

JWT_PRIVATE_KEY_PATH = os.getenv('JWT_PRIVATE_KEY_PATH')
JWT_PUBLIC_KEY_PATH = os.getenv('JWT_PUBLIC_KEY_PATH')


def read_key(path, name):
    if not path:
        raise ImproperlyConfigured(f'La ruta de la llave {name} JWT no está definida correctamente')

    if not Path(path).exists():
        raise ImproperlyConfigured(f'No se encontró la llave {name} en la ruta especificada')

    return Path(path).read_text()


JWT_PRIVATE_KEY = read_key(JWT_PRIVATE_KEY_PATH, 'privada')
JWT_PUBLIC_KEY = read_key(JWT_PUBLIC_KEY_PATH, 'publica')

SIMPLE_JWT = {
    'ALGORITHM': 'RS256',
    'SIGNING_KEY': JWT_PRIVATE_KEY,   
    'VERIFYING_KEY': JWT_PUBLIC_KEY,  
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),

    'AUTH_COOKIE': 'access_token',
    'AUTH_COOKIE_REFRESH': 'refresh_token',
    'AUTH_COOKIE_SECURE': True,
    'AUTH_COOKIE_HTTPONLY': True,
    'AUTH_COOKIE_PATH': '/',
    'AUTH_COOKIE_SAMESITE': 'None',
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
    'http://localhost:5173',
    'https://guitarzone.cl',
]


# Dominios de Cookies
SESSION_COOKIE_DOMAIN = '.guitarzone.cl'
CSRF_COOKIE_DOMAIN = '.guitarzone.cl'


# 4. Atributos de seguridad (Obligatorios para SameSite=None)
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'

CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_HTTPONLY = False  
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'

# 5. Confianza en Cloudflare
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')



VERIFY_URL_PATH = 'email-verification/'
SITE_URL
 