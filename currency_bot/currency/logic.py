from decimal import Decimal
import datetime
import requests
from .models import Currency

EXCHANGE_RATES_API_URL = 'https://api.exchangeratesapi.io/'


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
    base_currency = 'USD'

    if base_currency in (from_, to):
        if from_ == base_currency:
            currency = Currency.objects.filter(base=from_, target=to).latest('date')
            rate = currency.rate
        else:
            currency = Currency.objects.filter(base=to, target=from_).latest('date')
            rate = 1 / currency.rate
        return rate
    from_currency_rate = Currency.objects.filter(base=base_currency, target=from_).latest('date').rate
    to_currency_rate = Currency.objects.filter(base=base_currency, target=to).latest('date').rate
    return to_currency_rate / from_currency_rate
