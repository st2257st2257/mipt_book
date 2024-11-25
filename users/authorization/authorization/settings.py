from pathlib import Path
import os
import re

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('USERS_SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS
allowed_hosts_str = os.environ.get('ALLOWED_HOSTS')
if allowed_hosts_str:
    #Use a regular expression to handle comma-separated values, allowing for spaces
    allowed_hosts = [host.strip() for host in re.split(r',\s*', allowed_hosts_str)]
    ALLOWED_HOSTS = allowed_hosts
else:
    ALLOWED_HOSTS = ['localhost'] # Fallback to localhost if not set in .env
MAIN_HOST = os.environ.get('MAIN_HOST', 'mipt.site')


CORS_ALLOW_HEADERS = ['*']

# CORS_ORIGIN_ALLOW_ALL = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

CORS_ORIGIN_WHITELIST = [
    'https://127.0.0.1',
    'https://127.0.0.1:8000',
    'https://127.0.0.1:8088',
    'https://127.0.0.1:8083',
    'https://mipt.site'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'test',
    'rest_framework',
    'rest_framework.authtoken',
    'sslserver',
    'corsheaders',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

CORS_ORIGIN_ALLOW_ALL=True

ROOT_URLCONF = 'authorization.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'authorization.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     os.environ.get('USERS_DB_NAME',     'postgres_mipt_users'),
        'USER':     os.environ.get('USERS_DB_USER',     'postgres_mipt_users'),
        'PASSWORD': os.environ.get('USERS_DB_PASSWORD', 'postgres_mipt_users123'),
        'HOST':     os.environ.get('USERS_DB_HOST',     'pgdb_users'),
        'PORT':     os.environ.get('USERS_DB_PORT',     '5431')
    }
}

EMAIL_KEY = os.environ.get('EMAIL_KEY', 'hack_me_users')
USER_OAUTH_YANDEX_TOKEN = os.environ.get('USER_OAUTH_YANDEX_TOKEN', '')
TG_LOG_TOKEN = os.environ.get('TG_LOG_TOKEN', '')

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

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'main', 'static'),
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'main.User'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "debug.log",
        },
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug_file.log',
        },
        'info_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'info_file.log',
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'warning_file.log',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'error_file.log',
        },
        'critical_file': {
            'level': 'CRITICAL',
            'class': 'logging.FileHandler',
            'filename': 'critical_file.log',
        },
    },
    "root": {
        "handlers": ["console", "file", "debug_file", "info_file", "warning_file", "error_file", "critical_file"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

