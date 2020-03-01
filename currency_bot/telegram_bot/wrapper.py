from urllib.parse import urljoin
import requests
from django.urls import reverse
from django.conf import settings


def get_telegram_bot_url():
    telegram_token = getattr(settings, 'TELEGRAM_TOKEN')
    return f'https://api.telegram.org/bot{telegram_token}/'


def set_webhook(host):
    webhook_path = reverse('telegram:webhook')
    telegram_secret_path = getattr(settings, 'TELEGRAM_SECRET_PATH')
    if telegram_secret_path:
        webhook_path += telegram_secret_path + '/'

    url = urljoin(host, webhook_path)
    payload = {
        'url': url,
    }
    response = requests.post(f'{get_telegram_bot_url()}setWebhook', json=payload, timeout=5)
    return response.json()


def send_message(chat_id, text, parse_mode='HTML'):
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode,
    }
    response = requests.post(f'{get_telegram_bot_url()}sendMessage', json=payload, timeout=5)
    return response.json()


def send_photo(chat_id, photo):
    data = {
        'chat_id': chat_id,
    }
    files = {
        'photo': photo
    }
    response = requests.post(f'{get_telegram_bot_url()}sendPhoto', data=data, files=files, timeout=5)
    return response.json()
