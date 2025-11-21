from uuid import UUID

from apps.autoshows.models import AutoShowsStock
from apps.common.repositories import BaseRepository


class AutoShowsStockRepository(BaseRepository[AutoShowsStock]):
    model = AutoShowsStock

    def get_autoshow_stock(self, autoshow_id: UUID):
        return self.model.objects.filter(autoshow_id=autoshow_id, is_active=True)
