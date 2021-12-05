import uuid
from django.db import models


class Update(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    update_id = models.PositiveIntegerField()
    message = models.JSONField(null=True)
