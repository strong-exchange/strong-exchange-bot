import json
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest
from django.conf import settings
from .models import Update
from .chat import process_message


class TelegramWebhookView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        telegram_secret_path = getattr(settings, 'TELEGRAM_SECRET_PATH')
        if telegram_secret_path and kwargs.get('secret_path') != telegram_secret_path:
            raise Http404()

        # ToDo: add validation by self signed certificate

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.content_type != 'application/json' or not request.body:
            return HttpResponseBadRequest()

        data = json.loads(request.body.decode())

        # ToDo: Update for work with other type of updates
        message = data.get('message')
        if message:
            update, created = Update.objects.update_or_create(
                update_id=data.get('update_id'),
                defaults=dict(message=message)
            )
            if created:
                process_message(message)

        return HttpResponse()
