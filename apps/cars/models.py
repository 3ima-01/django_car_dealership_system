from uuid import uuid4

from django.db import models

from apps.common.models import AbstractBaseModel


class Cars(AbstractBaseModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    year = models.IntegerField()
    brand = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    color = models.CharField(max_length=64)
    body_type = models.CharField(max_length=64)
    engine_type = models.CharField(max_length=64)
    horse_power = models.IntegerField()
    properties = models.JSONField(null=True, default=dict)
