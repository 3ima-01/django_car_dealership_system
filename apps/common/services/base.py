from typing import Any
from uuid import UUID

from django.db import models
from django.shortcuts import get_object_or_404


class BaseService:
    model: models.Model = None

    def get_active(self, **kwargs) -> models.QuerySet:
        return self.model.objects.filter(is_active=True, **kwargs)

    def get_active_or_404(self, **kwargs) -> models.Model:
        return get_object_or_404(self.model, is_active=True, **kwargs)

    def create(self, data: dict[str, Any]):
        return self.model.objects.create(**data)

    def update(self, data: dict[str, Any], **kwargs):
        try:
            instance = self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            return

        for field, value in data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)

        instance.save()

        return instance

    def soft_delete(self, id: UUID):
        return self.model.objects.filter(id=id).update(is_active="False")
