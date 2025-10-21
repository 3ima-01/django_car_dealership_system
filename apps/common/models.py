from django.db import models


class Cars(models.Model):
    id = models.UUIDField(primary_key=True)
    year = models.IntegerField()
    brand = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    color = models.CharField(max_length=64)
    body_type = models.CharField()
    engine_type = models.CharField(max_length=64)
    horse_power = models.IntegerField()
    properties = models.JSONField(null=True, default=dict)


class AbstractBaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
