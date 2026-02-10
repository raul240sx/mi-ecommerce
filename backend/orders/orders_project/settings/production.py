from .base import *
from django.core.exceptions import ImproperlyConfigured


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False

if not SECRET_KEY:
    raise ImproperlyConfigured("La variable SECRET_KEY no está configurada en el entorno de producción.")


ALLOWED_HOSTS = [os.getenv('DOMAIN_NAME')]
CSRF_TRUSTED_ORIGINS = [f'https://{os.getenv('DOMAIN_NAME')}']



# BLOQUE DE SEGURIDAD 
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

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


FRONTEND_URL=os.getenv('FRONTEND_URL')



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Cambia esto:
STATIC_URL = '/static/orders/'
STATIC_ROOT = '/usr/src/app/staticfiles'



