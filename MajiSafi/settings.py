"""
Django settings for MajiSafi project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import dj_database_url
from environ import Env
env = Env()
Env.read_env()

ENVIRONMENT  = env('ENVIRONMENT', default="development")
# ENVIRONMENT = "production"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY', default="secret_key")

# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRONMENT == 'development':
    DEBUG = True
else:
    DEBUG = False
    
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])
CSRF_TRUSTED_ORIGINS = [ 'https://app-production-bad1.up.railway.app' ]


# Application definition
INSTALLED_APPS = [
    'django.contrib.sites',
    'accounts.apps.AccountsConfig',
    'supplier.apps.SupplierConfig',
    'services.apps.ServicesConfig',
    'marketplace.apps.MarketplaceConfig',
    'customers.apps.CustomersConfig',
    'orders.apps.OrdersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #Other Installations
    'cloudinary_storage',
    'cloudinary',
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'orders.request_object.RequestObjectMiddleware', # Custom Middleware created to access the request object in modles.py
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'MajiSafi.urls'

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
                'accounts.context_processors.get_supplier',
                'accounts.context_processors.get_user_profile',
                'accounts.context_processors.get_google_api',
                'marketplace.context_processors.get_cart_counter',
                'marketplace.context_processors.get_cart_amounts',
                'accounts.context_processors.get_paypal_client_id',


            ],
        },
    },
]

WSGI_APPLICATION = 'MajiSafi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


# Dockerize postgresdb
if ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'postgres',
            'PORT': 5432,
        }
    }
    # CELERY configuration docker
    CELERY_BROKER_URL = "redis://redis:6379/0"
else:
    DATABASES = {
        'default': dj_database_url.parse(env('DATABASE_URL', default='postgresql://'))
    }
    CELERY_BROKER_URL = env('REDIS_URL', default='redis://')


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR /'static'
STATICFILES_DIRS = [
    'MajiSafi/static'
]

MEDIA_URL = '/media/'

if ENVIRONMENT == 'development':
    MEDIA_ROOT = BASE_DIR /'media'
else:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME', default='your_cloudinary_name'),
    'API_KEY': env('CLOUDINARY_API_KEY', default='your_cloudinary_api_key'),
    'API_SECRET': env('CLOUDINARY_API_SECRET', default='your_cloudinary_secret_key'),
    }

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.User'

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Environment configurations
EMAIL_BACKEND = env('EMAIL_BACKEND', default="your_default_email_backend")
EMAIL_HOST = env('EMAIL_HOST', default="your_default_email_host")
EMAIL_PORT = env('EMAIL_PORT', cast=int, default=587)  # Example default port
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default="your_default_email_user")
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default="your_default_email_password")
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default="your_default_from_email")
GOOGLE_API_KEY = env('GOOGLE_API_KEY', default="your_default_google_api_key")
PAYPAL_CLIENT_ID= env('PAYPAL_CLIENT_ID', default="your_pay_pal_client_id")

# Block pop-ups using 3rd party services
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'

# CELERY Configuration
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Nairobi'
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

if ENVIRONMENT == 'development':
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis:6379/1",  # Use this in development
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env('REDIS_URL', default='redis://127.0.0.1:6379/1'),  # Use this in production
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }


# Logging Configurations
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'accounts': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
# Django-debug toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]



SITE_ID = 1