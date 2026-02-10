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