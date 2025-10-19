from django.db import models


class Cars(models.Model):
    id = models.UUIDField(primary_key=True)
    year = models.IntegerField()
    brand = models.TextField()
    model = models.TextField()
    color = models.TextField()
    body_type = models.TextField()
    engine_type = models.TextField()
    horse_power = models.IntegerField()
    properties = models.JSONField(null=True, default=dict)


class AbstractBaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
