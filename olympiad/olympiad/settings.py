"""
Django settings for olympiad project.

Generated by 'django-admin startproject' using Django 3.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

try:
    import storages
except ImportError:
    raise ImportError("django-storages is not installed or could not be found")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d!749*23^86bd^dejgv46gw_=^7awa*=v&vnkcecqui&9hpqg$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*", "olimp-team-olimp-web-7d5b.twc1.net", "olimp-olympiad.ru"]
CSRF_TRUSTED_ORIGINS = ["https://*", "http://*", 'https://*.olimp-olympiad.ru', 'https://*.127.0.0.1',
                        'http://*.olimp-olympiad.ru']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'debug_toolbar',
    'rest_framework',
    'rest_framework.authtoken',
    # My apps
    'olympiad',
    'main',
    'users',
    'api',
    'docs',
    'register',
    'classroom',
    'result',
    'django_filters',
    'channels',
    'chat',
    'schedule',
    'calendar_olimp',
    'corsheaders',
    'friendship',
    'friends',
    'storages',
    'image_cropping',
    'imagekit',
    'easy_thumbnails',

]
USE_TZ = False

THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
)

MIDDLEWARE = [
    # 'app.SimpleMiddleware.SimpleMiddleware'
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5174",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'olympiad.urls'

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
AUTH_USER_MODEL = 'users.User'

SESSION_COOKIE_AGE = 1209600  # 2 недели
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

ASGI_APPLICATION = 'olympiad.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': ['redis://:732301papa@147.45.236.130:6379/0'],
        },
    },
}

LOGIN_URL = 'users:login'
WSGI_APPLICATION = 'olympiad.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'default_db',
        'USER': 'gen_user',
        'PASSWORD': "Q/-*PaDx}9OJG#",
        'HOST': '147.45.236.124',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'  # SMTP-сервер вашего почтового провайдера
EMAIL_PORT = 2525  # Порт SMTP-сервера
EMAIL_USE_TLS = True  # Использовать TLS (рекомендуется для безопасности)
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'olimp-team@mail.ru'  # Ваш адрес электронной почты
EMAIL_HOST_PASSWORD = 'mgYJwJCtEYtM6DzyVRf1'  # Пароль от вашего email

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_INPUT_FORMATS = '%d-%m-%Y'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)


# Укажите путь к директории, где находятся статические файлы
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field


AWS_ACCESS_KEY_ID = 'Q5R69BCKUPU15EFXH076'
AWS_SECRET_ACCESS_KEY = 'X8dWZD8YTVbjyWgvBtP9igjphuAGG14X5c7TFfZi'
AWS_STORAGE_BUCKET_NAME = '387f7de3-599caebc-703e-4f34-abb7-b2a53cb494b2'  # замените на имя вашего бакета
AWS_S3_REGION_NAME = 'ru-1'
AWS_S3_ENDPOINT_URL = 'https://s3.timeweb.cloud'

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.timeweb.cloud'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False

# Ensure to specify path-style addressing
AWS_S3_ADDRESSING_STYLE = "path"

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

STATICFILES_STORAGE = 'olympiad.custom_storages.StaticStorage'
DEFAULT_FILE_STORAGE = 'olympiad.custom_storages.MediaStorage'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        # Добавьте другие методы аутентификации, если нужно, например, токены
        # 'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

LOGIN_URL = 'users:login'
