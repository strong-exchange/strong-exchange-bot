from currency.logic import load_latest_currency_rates
from .wrapper import send_message


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
    answer += '\n'.join(f'• {curreny.target} - {curreny.rate:.2f}' for curreny in currencies)
    send_message(message['chat']['id'], answer)


command_mapping = {
    '/start': say_hello,
    '/help': send_help_information,
    '/list': send_list_currencies,
    '/lst': send_list_currencies,
}


def process_message(message):
    if not message['text'].startswith('/'):
        return
    command = message['text'].split(' ', 1)[0]
    if command in command_mapping:
        command_mapping[command](message)
