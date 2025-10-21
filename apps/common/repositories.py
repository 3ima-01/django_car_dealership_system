from typing import Any
from uuid import UUID

from django.shortcuts import get_object_or_404


class BaseRepository:
    model = None

    def get_all(self):
        """Получить все записи"""
        return self.model.objects.all()

    def get_by_id(self, id: UUID):
        """Получить записи по ID, возвращает None если не найден"""
        try:
            return self.model.objects.get(pk=id)
        except self.model.DoesNotExist:
            return None

    def get_by_id_or_404(self, id: UUID):
        """Получить записи по ID, выбросить 404 если не найден (для DRF)"""
        return get_object_or_404(self.model, pk=id)

    def create(self, data: dict[str, Any]):
        """Создать новый автосалон"""
        return self.model.objects.create(**data)
