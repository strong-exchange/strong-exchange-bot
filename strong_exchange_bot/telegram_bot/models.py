import uuid
from django.db import models
from django.contrib.postgres.fields import JSONField


class Update(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    update_id = models.PositiveIntegerField()
    message = JSONField(null=True)

