from decimal import Decimal
from datetime import datetime, timedelta
import requests
from django.utils import timezone
from django.conf import settings
from .models import Currency

BASE_CURRENCY = 'USD'


def load_latest_currency_rates(force_reload=False) -> Currency.objects:
    # ToDo: to think maybe caching not required or use more fast storage
    # if less than 10 minutes since last update, don't make new request
    latest_currency = Currency.objects.order_by('-updated').first()
    if force_reload or not latest_currency or (timezone.now() - latest_currency.updated) > timedelta(minutes=10):
        response = requests.get(f'{settings.EXCHANGE_RATES_API_URL}latest', params={'base': 'USD'})
        data = response.json()
        date = datetime.strptime(data['date'], '%Y-%m-%d')
        for currency, value in data['rates'].items():
            Currency.objects.update_or_create(
                base=data['base'],
                target=currency,
                date=date,
                defaults=dict(rate=value,)
            )

    date = Currency.objects.latest('date').date

    return Currency.objects.filter(date=date)


def get_exchange_rate(from_: str, to: str) -> Decimal:
    currency_latest = load_latest_currency_rates()
    for currency in (from_, to,):
        if not currency_latest.filter(target=currency).exists():
            raise ValueError(f"Did't have rate for currency {currency}")

    if BASE_CURRENCY in (from_, to):
        if from_ == BASE_CURRENCY:
            currency = currency_latest.get(base=from_, target=to)
            rate = currency.rate
        else:
            currency = currency_latest.get(base=to, target=from_)
            rate = 1 / currency.rate
        return rate
    from_currency_rate = currency_latest.get(base=BASE_CURRENCY, target=from_).rate
    to_currency_rate = currency_latest.get(base=BASE_CURRENCY, target=to).rate
    return to_currency_rate / from_currency_rate


def get_currency_history(currencies, from_, to):
    params = {
        'base': BASE_CURRENCY,
        'symbols': ','.join(currencies),
        'start_at': from_,
        'end_at': to
    }
    response = requests.get(f'{settings.EXCHANGE_RATES_API_URL}history', params=params)
    return response.json()
