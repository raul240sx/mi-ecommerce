from .base import *


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'


ALLOWED_HOSTS = [
    'products-service',
    'users-service',
    'orders-service',
    'localhost',
    '127.0.0.1',
    '.app.github.dev',      # <- para permitir subdominios de Codespaces
    'casaserver',
    'overtenaciously-ordainable-davion.ngrok-free.dev'
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.app.github.dev',
    'https://localhost:7200'
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



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.base.custom_authentication.CustomAuthentication',
    ),

    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'


FRONTEND_URL=os.getenv('NGROK_URL')



# --- MERCADOPAGO CONFIG ---
MERCADOPAGO_PUBLIC_KEY = os.getenv('MP_PUBLIC_KEY')
MERCADOPAGO_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN')


SPECTACULAR_SETTINGS = {
    'TITLE': 'Orders API',
    'VERSION': '0.1.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'persistAuthorization': True,
    },
    'SWAGGER_UI_FAVICON_HREF': '/static/users/favicon.ico',
}