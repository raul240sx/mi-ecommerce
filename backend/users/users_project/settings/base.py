from django.core.exceptions import ImproperlyConfigured
from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv
from django.contrib.admin import AdminSite


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(BASE_DIR.parent / '.env')





# Personalización del admin
AdminSite.site_header = 'Guitar Zone Admin'
AdminSite.site_title = 'Guitar Zone'
AdminSite.index_title = 'Panel de Administración'



BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'apps.users',
    'apps.locations',
]

THIRD_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'simple_history',
    'drf_spectacular',
    'corsheaders',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



ROOT_URLCONF = 'users_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'users_project.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTH_USER_MODEL = 'users.User'

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



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


## CELERY
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis-service:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis-service:6379/1')

CELERY_TASK_DEFAULT_QUEUE = 'users_queue'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'


# SWAGGER
SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'none',
    'DEFAULT_SCHEME': 'https',
}

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]