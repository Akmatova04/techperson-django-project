

from pathlib import Path
from decouple import config
from django.core.exceptions import ImproperlyConfigured
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config('SECRET_KEY', default='django-insecure-YOUR_DEFAULT_FALLBACK_SECRET_KEY_HERE_CHANGE_ME')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS_STRING = config('ALLOWED_HOSTS', default='127.0.0.1,localhost')
ALLOWED_HOSTS = [s.strip() for s in ALLOWED_HOSTS_STRING.split(',')]
if DEBUG and '*' not in ALLOWED_HOSTS and '127.0.0.1' in ALLOWED_HOSTS: # Development үчүн '*' кошобуз
    ALLOWED_HOSTS.append('*')
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'learning_hub',
    'users',
    'crispy_forms',
    'crispy_bootstrap5',
   
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'education_core.urls' 

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'education_core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


LANGUAGE_CODE = config('LANGUAGE_CODE', default='ky-KG') 
TIME_ZONE = config('TIME_ZONE', default='Asia/Bishkek') 
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles_collected' # `collectstatic` үчүн

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'mediafiles'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default=None)
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default=None)
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER', default=None)

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER]):
    if DEBUG:
        print("\033[93mЭСКЕРТҮҮ:\033[0m .env файлында Twilio орнотуулары (ACCOUNT_SID, AUTH_TOKEN, PHONE_NUMBER) толук эмес же табылган жок. SMS жөнөтүү иштебейт.")
    else:
        raise ImproperlyConfigured(
            "Production үчүн Twilio орнотуулары (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER) .env файлында толук эмес!"
        )

LOGIN_REDIRECT_URL = config('LOGIN_REDIRECT_URL', default='/') # .env'ден алса болот
LOGOUT_REDIRECT_URL = config('LOGOUT_REDIRECT_URL', default='/') # .env'ден алса болот
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Же сиздин BASE_DIR аныктамаңыз
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
