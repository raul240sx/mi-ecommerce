from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR.parent / '.env')



# Application definition

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'apps.products',
    'apps.base',
]

THIRD_APPS = [
    'rest_framework',
    'simple_history',
    'drf_spectacular',
    'corsheaders',
]

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS

USERS_VERIFY_URL = 'http://users-service:8000/usuario/verify_token/'



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'apps.base.middleware.JWTVerificationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'products_project.urls'

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

WSGI_APPLICATION = 'products_project.wsgi.application'

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- JWT CONFIG ---

CALL_USERS_SERVICE = os.getenv('CALL_USERS_SERVICE', False)
TOKEN_VERIFY_URL = os.getenv('TOKEN_VERIFY_URL')
INTERNAL_SERVICE_KEY= os.getenv('INTERNAL_SERVICE_KEY')
JWT_PUBLIC_KEY_PATH = os.getenv('JWT_PUBLIC_KEY_PATH')

def read_key(path):
    if not path:
        raise ImproperlyConfigured(f'La ruta de la llave JWT no está definida correctamente')

    if not Path(path).exists():
        raise ImproperlyConfigured(f"No se encontró la llave pública en la ruta especificada")

    return Path(path).read_text()


JWT_PUBLIC_KEY = read_key(JWT_PUBLIC_KEY_PATH)



# --- MEDIA CONFIG ---

MEDIA_URL = '/media/'

MEDIA_ROOT = os.getenv('MEDIA_ROOT_PATH', '/usr/src/app/media')


STATICFILES_DIRS = [
    BASE_DIR / 'static',
]