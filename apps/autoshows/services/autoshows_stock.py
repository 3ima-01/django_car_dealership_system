from uuid import UUID

from django.db.models import QuerySet

from apps.autoshows.models import AutoShowsStock
from apps.autoshows.repositories.autoshows_stock import AutoShowsStockRepository


class AutoShowsStockService:
    def __init__(self):
        self.repository = AutoShowsStockRepository()

    def get_autoshow_stock(self, autoshow_id: UUID) -> QuerySet[AutoShowsStock]:
        return self.repository.get_autoshow_stock(autoshow_id)
