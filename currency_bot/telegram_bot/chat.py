from decimal import Decimal
from currency.logic import load_latest_currency_rates, get_exchange_rate
from .wrapper import send_message


currency_shortcuts = {
    'CAD': ('CA$', 'C$',),
    'HKD': ('HK$',),
    'PHP': ('₱',),
    'GBP': ('£',),
    'RUB': ('рублей', 'рубли', 'рублях', 'р', '₽'),
    'THB': ('baht', '฿',),
    'EUR': ('euro', '€',),
    'MYR': ('ringgit', 'MR',),
    'USD': ('US$', '$',),
    'SGD': ('SG$', 'S$',),
    'AUD': ('AU$', 'A$'),
}
shortcut_currency = {}
for currency, shortcuts in currency_shortcuts.items():
    for shortcut in shortcuts:
        shortcut_currency[shortcut.upper()] = currency


def parse_exchange_line(text: str) -> (Decimal, str, str):
    try:
        amount_from, to = text.upper().split('TO')
    except ValueError:
        raise ValueError('Invalid format.')
    to = to.strip()
    from_ = amount_from.strip('0123456789. ')
    if not from_:
        raise ValueError('There is not found currency from which exchange is made.')
    amount = ''.join(amount_from.split(from_)).strip() or 1

    to = shortcut_currency.get(to, to)
    from_ = shortcut_currency.get(from_, from_)

    if not to:
        raise ValueError("Couldn't parse target currency.")
    return Decimal(amount), from_, to


def say_hello(message):
    answer = (
        f"Hello, {message['chat']['first_name']}!\n"
        f"I'm <b>Currency Bot</b> and can offer various information about the rate of currencies.\n\n"
        f"For more type: /help"
    )
    send_message(message['chat']['id'], answer)


def send_help_information(message):
    answer = (
        "<b>Information about supported commands</b>\n"
        "/list or /lst - returns a list of all available rates\n"
        "/exchange - convert the first currency to the second\n"
        "/history - show graph of selected currencies for the last 7 days\n"
        "/help - list of supported commands"
    )
    send_message(message['chat']['id'], answer)


def send_list_currencies(message):
    currencies = load_latest_currency_rates()
    answer = f"Currencies for {currencies[0].date.strftime('%d %B %Y')}\n"
    answer += '\n'.join(f'• {currency.target}: {currency.rate:.2f}' for currency in currencies)
    send_message(message['chat']['id'], answer)


def exchange_currency(message):
    format_recommendation = 'Please use format like this: \n/exchange 10 USD to THB.'

    chat_id = message['chat']['id']
    exchange_message_text = message['text'].lstrip('/exchange').strip()
    if not exchange_message_text:
        return send_message(chat_id, format_recommendation)
    try:
        amount, from_, to = parse_exchange_line(exchange_message_text)
    except ValueError as ex:
        return send_message(chat_id, f'{str(ex)}\n{format_recommendation}')
    try:
        exchanged_amount = amount * get_exchange_rate(from_, to)
    except ValueError as ex:
        return send_message(chat_id,  f'{str(ex)}')
    return send_message(chat_id, f'{amount:.2f}  {from_} ~ {exchanged_amount:.2f} {to}')


command_mapping = {
    '/start': say_hello,
    '/help': send_help_information,
    '/list': send_list_currencies,
    '/lst': send_list_currencies,
    '/exchange': exchange_currency,
}


def process_message(message):
    if not message['text'].startswith('/'):
        return
    command = message['text'].split(' ', 1)[0]
    if command in command_mapping:
        command_mapping[command](message)
