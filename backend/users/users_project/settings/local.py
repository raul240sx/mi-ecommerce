from .base import *


DEBUG = True

ALLOWED_HOSTS = [
    'users-service',       # contenedor Docker interno
    'products-service',    # contenedor Docker interno
    'orders-service',      # contenedor Docker interno
    'localhost',
    '127.0.0.1',
    '.app.github.dev'      # <- para permitir subdominios de Codespaces
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

