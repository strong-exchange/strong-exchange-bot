from telegram_bot.wrapper import set_webhook
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Set webhook host for telegram'

    def add_arguments(self, parser):
        parser.add_argument('host', help='url of server with bot', type=str)

    def handle(self, host, *args, **options):
        self.stdout.write(f'Registering telegram webhook for {host}.')

        data = set_webhook(host)
        if data.get('error_code') == 404:
            self.stdout.write(self.style.ERROR(f'Unsuccessfully: {data}.'))
            self.stdout.write('Please check that is the application server is running.')
            return

        self.stdout.write(self.style.SUCCESS(f'Successfully: {data}.'))
