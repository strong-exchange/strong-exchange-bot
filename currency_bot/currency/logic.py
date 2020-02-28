import requests
from .models import Currency


def load_latest_currency_rates():
    response = requests.get('https://api.exchangeratesapi.io/latest', params={'base': 'USD'})
    response.json()
