import json
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import Http404, HttpResponse
from django.conf import settings
from .chat import process_message


class TelegramWebhookView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        telegram_secret_path = getattr(settings, 'TELEGRAM_SECRET_PATH')
        if telegram_secret_path and kwargs.get('secret_path') != telegram_secret_path:
            raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.content_type == 'application/json' and request.body:
            data = json.loads(request.body.decode())
            message = data.get('message')
            if message:
                process_message(message)

        return HttpResponse()
