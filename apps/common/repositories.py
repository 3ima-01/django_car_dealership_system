from typing import Any, Generic, TypeVar
from uuid import UUID

from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404

ModelType = TypeVar("ModelType", bound=Model)


class BaseRepository(Generic[ModelType]):
    model: type[ModelType]

    def get_all(self) -> QuerySet[ModelType]:
        """Get all active data (is_active=True)"""
        return self.model.objects.filter(is_active=True)

    def get_all_with_inactive(self) -> QuerySet[ModelType]:
        """Get all data including inactive ones"""
        return self.model.objects.all()

    def get_by_id(self, id: UUID) -> ModelType | None:
        """Get data by ID, return None If doesn`t exist"""
        try:
            return self.model.objects.get(pk=id, is_active=True)
        except self.model.DoesNotExist:
            return None

    def get_by_id_or_404(self, id: UUID) -> ModelType:
        """Get data by ID, return 404 if doesn`t exist (for DRF)"""
        return get_object_or_404(self.model, pk=id, is_active=True)

    def create(self, data: dict[str, Any]):
        """Create new data"""
        return self.model.objects.create(**data)

    def update(self, id: UUID, data: dict[str, Any]):
        """Update data by id"""
        return self.model.objects.filter(pk=id, is_active=True).update(**data)

    def soft_delete(self, id: UUID):
        """Soft delete: set is_active=False"""
        return self.model.objects.filter(pk=id, is_active=True).update(is_active=False)
