from decimal import Decimal


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
