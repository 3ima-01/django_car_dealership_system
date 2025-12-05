from uuid import UUID

from django.db.models import QuerySet

from apps.autoshows.models import AutoShowsStock


class AutoShowsStockService:
    def __init__(self):
        self.model = AutoShowsStock

    def get_autoshow_stock(self, autoshow_id: UUID) -> QuerySet[AutoShowsStock]:
        return self.model.objects.filter(autoshow_id=autoshow_id)
