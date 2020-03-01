import json
import responses
from django.test import TestCase, override_settings
from .wrapper import set_webhook


class TestTelegramSetWebhook(TestCase):
    def setUp(self) -> None:
        responses.add(
            responses.POST,
            'https://api.telegram.org/bot_not_valid_token_/setWebhook',
            json={
                'description': 'Not Found',
                'error_code': 404,
                'ok': False
            },
            content_type='application/json'
        )
        responses.add(
            responses.POST,
            'https://api.telegram.org/bot_valid_token_/setWebhook',
            json={
                'ok': True,
                'result': True,
                'description': 'Webhook was set'
            },
            content_type='application/json'
        )


    @override_settings(TELEGRAM_TOKEN='_not_valid_token_')
    @responses.activate
    def test_cant_set_webhook_with_not_valid_token(self) -> None:
        data = set_webhook('https://example.com/')

        self.assertEqual({
            'description': 'Not Found',
            'error_code': 404,
            'ok': False
        }, data)

    @override_settings(TELEGRAM_TOKEN='_not_valid_token_')
    @responses.activate
    def test_registering_webhook_not_pass_secret_path_if_not_necessary(self):
        set_webhook('https://example.com/')

        self.assertEqual(
            'https://example.com/telegram/webhook/',
            json.loads(responses.calls[0].request.body.decode())['url']
        )

    @override_settings(TELEGRAM_TOKEN='_not_valid_token_')
    @override_settings(TELEGRAM_SECRET_PATH='secret_path')
    @responses.activate
    def test_registering_webhook_pass_secret_path_if_necessary(self):
        set_webhook('https://example.com/')

        self.assertEqual(
            'https://example.com/telegram/webhook/secret_path/',
            json.loads(responses.calls[0].request.body.decode())['url']
        )

    @override_settings(TELEGRAM_TOKEN='_valid_token_')
    @responses.activate
    def test_can_set_webhook(self) -> None:
        data = set_webhook('https://example.com/')
        self.assertEqual({
            'ok': True,
            'result': True,
            'description': 'Webhook was set'
        }, data)


class TestTelegramWebhook(TestCase):
    def setUp(self) -> None:
        responses.add(
            responses.POST,
            'https://api.telegram.org/botNone/sendMessage',
            json={
                'ok': True,
                'result': {
                    'message_id': 15,
                    'from': {
                        'id': 1046039193, 'is_bot': True,
                        'first_name': 'Strong Currency', 'username': 'StrongCurrencyBot'
                    },
                    'chat': {
                        'id': 999199923, 'first_name': 'Egor', 'username': 'NickName', 'type': 'private'
                    },
                    'date': 1583036649,
                    'text': "Hello, Egor!\nI'm Currency Bot and can offer various information about the rate "
                            "of currencies.\n\nFor more type: /help",
                    'entities': [
                        {'offset': 17, 'length': 12, 'type': 'bold'},
                        {'offset': 110, 'length': 5, 'type': 'bot_command'}
                    ]
                }
            },
            content_type='application/json'
        )

    start_message_payload = {
        'update_id': 496375863,
        'message': {
            'message_id': 1,
            'from': {'id': 999199923, 'is_bot': False, 'first_name': 'Egor', 'username': 'NickName'},
            'chat': {'id': 999199923, 'first_name': 'Egor', 'username': 'NickName', 'type': 'private'},
            'date': 1583026077,
            'text': '/start',
            'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]
        }
    }

    def test_if_request_webhook_api_without_telegram_secret_path_not_get_404_error_if_secret_path_not_required(self):
        response = self.client.post('/telegram/webhook/')
        self.assertEqual(200, response.status_code)

    @override_settings(TELEGRAM_SECRET_PATH='secret_path')
    def test_if_request_webhook_api_without_telegram_secret_path_get_404_error_if_secret_path_required(self):
        response = self.client.post('/telegram/webhook/')
        self.assertEqual(404, response.status_code)

        response = self.client.post('/telegram/webhook/wrong_secret_path/')
        self.assertEqual(404, response.status_code)

        response = self.client.post('/telegram/webhook/secret_path/')
        self.assertEqual(200, response.status_code)

    @responses.activate
    def test_can_process_incoming_message_start(self):
        response = self.client.post(
            '/telegram/webhook/', data=self.start_message_payload, content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

        telegram_message_api_response = json.loads(responses.calls[0].request.body.decode())
        self.assertEqual(
            999199923,
            telegram_message_api_response['chat_id']
        )

    # ToDo: not process messages twice
