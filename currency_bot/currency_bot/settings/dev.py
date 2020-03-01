import os
from .base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hyj1_a$idj45a*_zq%-$zo33nyz8u1c(f^d58_p5whx#ugic^x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'currency_bot',
        'USER': 'currency_bot',
        'PASSWORD': 'currency_bot',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Telegram Token

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_SECRET_PATH = os.environ.get('TELEGRAM_SECRET_PATH')
