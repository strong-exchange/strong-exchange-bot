from decimal import Decimal
from datetime import date
import responses
from django.test import TestCase
from currency.helpers import parse_exchange_line
from .models import Currency
from .logic import load_latest_currency_rates, get_exchange_rate


class TestCurrency(TestCase):
    latest = {'rates': {'CAD': 1.3349142649, 'HKD': 7.7942356804, 'ISK': 127.0521707406, 'PHP': 50.8637358628,
                        'DKK': 6.8154870485, 'HUF': 308.6191171105, 'CZK': 23.0600145932, 'GBP': 0.7752188982,
                        'RON': 4.3870850055, 'SEK': 9.6454761036, 'IDR': 14034.9963516965, 'INR': 71.6326158336,
                        'BRL': 4.4668916454, 'RUB': 65.7654140825, 'HRK': 6.8063662897, 'JPY': 109.8686610726,
                        'THB': 31.6499452754, 'CHF': 0.9692630427, 'EUR': 0.9120758847, 'MYR': 4.2105071142,
                        'BGN': 1.7838380153, 'TRY': 6.1599781102, 'CNY': 7.0059284933, 'NOK': 9.3869025903,
                        'NZD': 1.5802626779, 'ZAR': 15.3611820503, 'USD': 1.0, 'MXN': 19.3908245166,
                        'SGD': 1.3949288581, 'AUD': 1.520612915, 'ILS': 3.4358810653, 'KRW': 1211.0817219993,
                        'PLN': 3.9332360452}, 'base': 'USD', 'date': '2020-02-27'}

    @staticmethod
    def create_currency() -> None:
        Currency.objects.create(
            base='USD',
            target='EUR',
            rate=Decimal('1.2'),
            date=date(2020, 2, 2),
        )
        Currency.objects.create(
            base='USD',
            target='USD',
            rate=Decimal('1'),
            date=date(2020, 2, 3),
        )
        Currency.objects.create(
            base='USD',
            target='EUR',
            rate=Decimal('1.238'),
            date=date(2020, 2, 3),
        )
        Currency.objects.create(
            base='USD',
            target='HKD',
            rate=Decimal('7.7942356804'),
            date=date(2020, 2, 3),
        )
        Currency.objects.create(
            base='USD',
            target='RUB',
            rate=Decimal('65.7654140825'),
            date=date(2020, 2, 3),
        )

    @responses.activate
    def test_load_currency(self):
        responses.add(
            responses.GET,
            'https://api.exchangeratesapi.io/latest?base=USD',
            json=self.latest,
            content_type='application/json'
        )

        currency_qty = Currency.objects.count()

        currencies = load_latest_currency_rates()

        self.assertEqual(currency_qty + 33, Currency.objects.count())
        self.assertEqual(currencies[0].base, 'USD')
        self.assertEqual(currencies[0].target, 'CAD')
        self.assertEqual(str(currencies[0].rate), '1.3349142649')

    @responses.activate
    def test_load_currency_just_once(self):
        responses.add(
            responses.GET,
            'https://api.exchangeratesapi.io/latest?base=USD',
            json=self.latest,
            content_type='application/json',
        )

        currency_qty = Currency.objects.count()

        load_latest_currency_rates()
        load_latest_currency_rates()
        load_latest_currency_rates()

        self.assertEqual(currency_qty + 33, Currency.objects.count())

    def test_can_exchange_from_usd_to_eur(self):
        self.create_currency()
        rate = get_exchange_rate('USD', 'EUR')
        self.assertTrue(str(rate).startswith('1.238'))

    def test_can_exchange_from_eur_to_usd(self):
        self.create_currency()
        rate = get_exchange_rate('EUR', 'USD')
        self.assertEqual('0.8077544426494345718901453958', str(rate))

    def test_can_exchange_hkd_to_rur(self):
        self.create_currency()
        rate = get_exchange_rate('RUB', 'HKD')
        self.assertEqual(str(rate), '0.1185157242471316724260511311')


class TestCurrencyExchange(TestCase):
    def test_can_parse_currency_exchange_line_with_full_specified_names(self):
        amount, from_, to = parse_exchange_line('10 USD to CAD')
        self.assertEqual(10, amount)
        self.assertEqual('USD', from_)
        self.assertEqual('CAD', to)

    def test_can_parse_currency_exchange_line_with_shortcuts(self):
        amount, from_, to = parse_exchange_line('$10 to CAD')
        self.assertEqual(10, amount)
        self.assertEqual('USD', from_)
        self.assertEqual('CAD', to)

        amount, from_, to = parse_exchange_line('10 CAD to $')
        self.assertEqual(10, amount)
        self.assertEqual('CAD', from_)
        self.assertEqual('USD', to)

    def test_can_parse_currency_exchange_line_with_decimal_value(self):
        amount, from_, to = parse_exchange_line('12.7531 USD to CAD')
        self.assertEqual('12.7531', str(amount))
        self.assertEqual('USD', from_)
        self.assertEqual('CAD', to)

    # ToDo: add functionality for parse numbers with semicolon as decimal point indicator

    def test_can_parse_currency_exchange_line_without_whitespaces(self):
        amount, from_, to = parse_exchange_line('12.7531USDtoCAD')
        self.assertEqual('12.7531', str(amount))
        self.assertEqual('USD', from_)
        self.assertEqual('CAD', to)

    def test_can_parse_currency_exchange_line_register_of_symbols_not_have_meaning(self):
        amount, from_, to = parse_exchange_line('10 Usd to cAD')
        self.assertEqual(10, amount)
        self.assertEqual('USD', from_)
        self.assertEqual('CAD', to)

    def test_can_parse_currency_exchange_line_without_amount(self):
        amount, from_, to = parse_exchange_line('USD to CAD')
        self.assertEqual(1, amount)
        self.assertEqual('USD', from_)
        self.assertEqual('CAD', to)

    def test_raise_error_if_cant_parse_currency_exchange_line(self):
        with self.assertRaises(ValueError):
            parse_exchange_line('')

        with self.assertRaises(ValueError):
            parse_exchange_line('USD to')

        with self.assertRaises(ValueError):
            parse_exchange_line('to USD')
