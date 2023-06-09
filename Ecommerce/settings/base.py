import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
print("base dir path", BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(BASE_DIR, 'secret_key.txt')) as f:
    SECRET_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



# PAYU SECRET

with open(os.path.join(BASE_DIR, 'client_secret.txt')) as f:
    CLIENT_SECRET = f.read().strip()



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App',
    'crispy_forms',
    'crispy_bootstrap5',
    "phonenumber_field",
    'requests',
    'django_filters',
    'storages',
    'rest_framework',
    'Dashboard',
    'Api',
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

ROOT_URLCONF = 'Ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'Ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# static files

STATIC_URL = 'static/'
MEDIA_URL = 'images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

LOGIN_REDIRECT_URL = 'index'

# crispy forms

CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"


LANGUAGE_CODE = 'pl'
TIME_ZONE = 'Europe/Berlin'
USE_L10N = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 604800


# email

with open(os.path.join(BASE_DIR, 'password_email.txt')) as f:
    PASSWORD_EMAIL = f.read().strip()


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'kubalonekk99@gmail.com'
EMAIL_HOST_PASSWORD = PASSWORD_EMAIL
EMAIL_USE_TLS = True


# s3bucket aws

with open(os.path.join(BASE_DIR, 'AWS_SECRET_KEY.txt')) as f:
    AWS_SECRET_KEY = f.read().strip()
    
with open(os.path.join(BASE_DIR, 'AWS_ACCESS_KEY.txt')) as f:
    AWS_ACCESS_KEY = f.read().strip()


AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = AWS_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = 'ecommerce-online-main'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_QUERYSTRING_AUTH = False


