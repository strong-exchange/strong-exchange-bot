from decimal import Decimal
from datetime import timedelta
import datetime
import requests
from django.utils import timezone
from .models import Currency

EXCHANGE_RATES_API_URL = 'https://api.exchangeratesapi.io/'
BASE_CURRENCY = 'USD'


def load_latest_currency_rates() -> list:
    response = requests.get(f'{EXCHANGE_RATES_API_URL}latest', params={'base': 'USD'})
    data = response.json()
    date = datetime.datetime.strptime(data['date'], '%Y-%m-%d')

    currency_instances = []
    for currency, value in data['rates'].items():
        currency_instance, created = Currency.objects.update_or_create(
            base=data['base'],
            target=currency,
            date=date,
            defaults=dict(rate=value,)
        )
        currency_instances.append(currency_instance)

    return currency_instances


def get_exchange_rate(from_: str, to: str) -> Decimal:
    for currency in (from_, to,):
        if not Currency.objects.filter(target=currency).exists():
            raise ValueError(f"Did't have rate for currency {currency}")

    if BASE_CURRENCY in (from_, to):
        if from_ == BASE_CURRENCY:
            currency = Currency.objects.filter(base=from_, target=to).latest('date')
            rate = currency.rate
        else:
            currency = Currency.objects.filter(base=to, target=from_).latest('date')
            rate = 1 / currency.rate
        return rate
    from_currency_rate = Currency.objects.filter(base=BASE_CURRENCY, target=from_).latest('date').rate
    to_currency_rate = Currency.objects.filter(base=BASE_CURRENCY, target=to).latest('date').rate
    return to_currency_rate / from_currency_rate


def get_currency_history(currencies, from_, to):
    params = {
        'base': BASE_CURRENCY,
        'symbols': ','.join(currencies),
        'start_at': from_,
        'end_at': to
    }
    response = requests.get(f'{EXCHANGE_RATES_API_URL}history', params=params)
    return response.json()
