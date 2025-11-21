from typing import Any
from uuid import UUID

from django.db.models import QuerySet

from apps.autoshows.models import AutoShows
from apps.autoshows.repositories.autoshows import AutoShowsRepository


class AutoShowsService:
    def __init__(self):
        self.repository = AutoShowsRepository()

    def get_all_autoshows(self) -> QuerySet[AutoShows]:
        return self.repository.get_all()

    def get_autoshow_by_id(self, auto_show_id: UUID) -> AutoShows | None:
        autoshow = self.repository.get_by_id(auto_show_id)
        return autoshow

    def get_autoshow_by_id_or_404(self, auto_show_id: UUID) -> AutoShows:
        return self.repository.get_by_id_or_404(auto_show_id)

    def create_autoshow(self, auto_show_data: dict[str, Any]):
        return self.repository.create(auto_show_data)

    def update_autoshow(self, auto_show_id: UUID, auto_show_data: dict[str, Any]):
        return self.repository.update(auto_show_id, auto_show_data)

    def soft_delete_autoshow(self, auto_show_id: UUID):
        return self.repository.soft_delete(auto_show_id)
