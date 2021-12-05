import os
import dj_database_url
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '_=PLACEHOLDER=_')  # REQUIRED! FOR COLLECT STATIC

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', 0))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DB_SSL_REQUIRE = bool(int(os.environ.get('DB_SSL_REQUIRE', 1)))
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=DB_SSL_REQUIRE)
}

# Telegram Token

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
TELEGRAM_SECRET_PATH = os.environ.get('TELEGRAM_SECRET_PATH')


# Entrypoint for currency rates

EXCHANGE_RATES_API_URL = os.environ.get('EXCHANGE_RATES_API_URL')
