from .base import *


DEBUG = True

ALLOWED_HOSTS = [
    'products-service',
    'users-service',
    'orders-service',
    'localhost',
    '127.0.0.1',
    '.app.github.dev'
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.app.github.dev',
    'https://localhost:7100'
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

