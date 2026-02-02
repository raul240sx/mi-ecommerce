from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(BASE_DIR.parent / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'


# Application definition

BASE_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = []

THIRD_APPS = []

INSTALLED_APPS = BASE_APPS + LOCAL_APPS + THIRD_APPS



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'orders_project.urls'

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

WSGI_APPLICATION = 'orders_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



INTERNAL_SERVICE_KEY= os.getenv('INTERNAL_SERVICE_KEY')



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

SIMPLE_JWT = {
    'ALGORITHM': 'RS256',   
    'VERIFYING_KEY': JWT_PUBLIC_KEY,  
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'USER_ID_FIELD': 'user_id',
    'USER_ID_CLAIM': 'user_id',
}


# --- MEDIA CONFIG ---

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




# --- MERCADOPAGO CONFIG ---
MERCADOPAGO_PUBLIC_KEY = os.getenv('MP_PUBLIC_KEY')
MERCADOPAGO_ACCESS_TOKEN = os.getenv('MP_ACCESS_TOKEN')