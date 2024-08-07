"""
Настройки Django для проекта olympiad.

Сгенерировано командой 'django-admin startproject' с использованием Django 3.2.15.

Для получения дополнительной информации о данном файле, см.
https://docs.djangoproject.com/en/3.2/topics/settings/

Для полного списка настроек и их значений, см.
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
from django.contrib.messages import constants as message_constants

# Убедимся, что модуль django-storages установлен
try:
    import storages
except ImportError:
    raise ImportError("django-storages не установлен или не найден")

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Основные настройки безопасности и режима отладки
SECRET_KEY = 'django-insecure-d!749*23^86bd^dejgv46gw_=^7awa*=v&vnkcecqui&9hpqg$'
DEBUG = False
ALLOWED_HOSTS = ["*", "olimp-team-olimp-web-7d5b.twc1.net", "olimp-olympiad.ru"]

# Интернационализация
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Asia/Yekaterinburg'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Формат ввода дат
DATE_INPUT_FORMATS = '%d-%m-%Y'

# Настройки пользовательской модели пользователя
AUTH_USER_MODEL = 'users.User'

# Настройки сессий
SESSION_COOKIE_AGE = 1209600  # 2 недели
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# URL для перенаправления при входе в систему
LOGIN_URL = 'users:login'

# Доверенные источники CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://*", "http://*", 'https://*.olimp-olympiad.ru', 'https://*.127.0.0.1',
    'http://*.olimp-olympiad.ru'
]

# Установленные приложения
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
    # Мои приложения
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
    # 'easy_thumbnails',
    'school',
    'raiting_system',
    'silk',
]

# Настройки обработки миниатюр
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
)

# Определение используемых посредников (middleware)
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'silk.middleware.SilkyMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# Настройки сообщений
MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}

# Разрешенные источники для CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5174",
]
CORS_ORIGIN_ALLOW_ALL = True

# Настройки REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Корневой URL-конфиг проекта
ROOT_URLCONF = 'olympiad.urls'

# Настройки шаблонов
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

# Настройка ASGI и WSGI приложений
ASGI_APPLICATION = 'olympiad.asgi.application'
WSGI_APPLICATION = 'olympiad.wsgi.application'

# Настройки Channel Layers
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': ['redis://:732301papa@147.45.236.130:6379/0'],
        },
    },
}

# Настройки базы данных
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'olimp_olympiad',
#         'USER': 'gen_user',
#         'PASSWORD': "Q/-*PaDx}9OJG#",
#         'HOST': '147.45.236.124',
#         'PORT': '3306',
#         'TEST': {
#             'NAME': 'test_olimp_olympiad',  # Укажите имя тестовой базы данных
#             'MIRROR': 'default',  # Зеркалирование основной базы данных
#         },
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Валидация паролей
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

# Настройки электронной почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'olimp-team@mail.ru'
EMAIL_HOST_PASSWORD = 'mgYJwJCtEYtM6DzyVRf1'
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Настройки AWS S3 для хранения файлов
AWS_ACCESS_KEY_ID = 'Q5R69BCKUPU15EFXH076'
AWS_SECRET_ACCESS_KEY = 'X8dWZD8YTVbjyWgvBtP9igjphuAGG14X5c7TFfZi'
AWS_STORAGE_BUCKET_NAME = '387f7de3-599caebc-703e-4f34-abb7-b2a53cb494b2'
AWS_S3_REGION_NAME = 'ru-1'
AWS_S3_ENDPOINT_URL = 'https://s3.timeweb.cloud'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.timeweb.cloud'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
AWS_S3_ADDRESSING_STYLE = "path"

STATICFILES_LOCATION = 'static'
MEDIAFILES_LOCATION = 'media'

STATICFILES_STORAGE = 'olympiad.custom_storages.StaticStorage'
DEFAULT_FILE_STORAGE = 'olympiad.custom_storages.MediaStorage'

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Укажите путь к директории, где находятся статические файлы
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = 'staticfiles/'
# Статические файлы (CSS, JavaScript, изображения)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Идентификатор сайта
SITE_ID = 1
