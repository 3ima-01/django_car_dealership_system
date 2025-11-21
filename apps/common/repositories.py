from typing import Any, Generic, TypeVar
from uuid import UUID

from django.db import models
from django.shortcuts import get_object_or_404

ModelType = TypeVar("ModelType", bound=models.Model)


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def get_all(self) -> models.QuerySet[ModelType]:
        """Get all active data (is_active=True)"""
        return self.model._default_manager.filter(is_active=True)

    def get_by_filter(self, **kwargs):
        """Get all data by filter"""
        return self.model._default_manager.filter(**kwargs)

    def get_by_filter_or_404(self, **kwargs):
        """Get all data by filter, return 404 if doesn`t exist (for DRF)"""
        return get_object_or_404(self.model, **kwargs)

    def get_all_with_inactive(self) -> models.QuerySet[ModelType]:
        """Get all data including inactive ones"""
        return self.model._default_manager.all()

    def create(self, data: dict[str, Any]):
        """Create new data"""
        return self.model._default_manager.create(**data)

    def update(self, id: UUID, data: dict[str, Any]):
        """Update data by id"""
        return self.model._default_manager.filter(pk=id, is_active=True).update(**data)

    def soft_delete(self, id: UUID):
        """Soft delete: set is_active=False"""
        return self.model._default_manager.filter(pk=id, is_active=True).update(is_active=False)
