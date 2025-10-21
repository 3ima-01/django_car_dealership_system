from typing import Any
from uuid import UUID

from apps.autoshows.repositories.autoshows import AutoShowsNotFoundException, AutoShowsRepository


class AutoShowsService:
    def __init__(self):
        self.repository = AutoShowsRepository()

    def get_all_autoshows(self):
        """Получить все автосалоны"""
        return self.repository.get_all()

    def get_autoshow_by_id(self, auto_show_id: UUID):
        """Получить автосалон по ID"""
        autoshow = self.repository.get_by_id(auto_show_id)
        if autoshow is None:
            raise AutoShowsNotFoundException(f"Auto show with id {auto_show_id} not found")
        return autoshow

    def get_autoshow_by_id_or_none(self, auto_show_id: UUID):
        """Получить автосалон по ID или None"""
        return self.repository.get_by_id(auto_show_id)

    def create_autoshow(self, auto_show_data: dict[str, Any]):
        """Создать новый автосалон"""
        return self.repository.create(auto_show_data)
