from .base import *


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = [
    'users-service',       # contenedor Docker interno
    'products-service',    # contenedor Docker interno
    'orders-service',      # contenedor Docker interno
    'localhost',
    '127.0.0.1',
    '.app.github.dev',      # <- para permitir subdominios de Codespaces
    'casaserver',
    '192.168.1.201',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://192.168.1.201:5173",
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.app.github.dev',  # wildcard de Codespaces
    'https://localhost:7000',
]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'




SITE_URL = 'http://192.168.1.201:3000'
SITE_NAME = 'Guitar Rage'

VERIFY_URL_PATH = 'auth/verify-email'
RESET_URL_PATH = 'auth/password-reset-confirm'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'proyectos.test1995@gmail.com'
EMAIL_HOST_PASSWORD = 'nkys erds bpfw iyin'
DEFAULT_FROM_EMAIL = 'Verificación App <proyectos.test1995@gmail.com>'


# --- MEDIA CONFIG ---

MEDIA_URL = '/media/'

MEDIA_ROOT = os.getenv('MEDIA_ROOT_PATH', '/usr/src/app/media')


SPECTACULAR_SETTINGS = {
    'TITLE': 'Users API',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    'SWAGGER_UI_FAVICON_HREF': '/static/users/favicon.ico',
}


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
    "ALGORITHM": 'RS256',
    "SIGNING_KEY": JWT_PRIVATE_KEY,   
    "VERIFYING_KEY": JWT_PUBLIC_KEY,  
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ('Bearer',),
}
