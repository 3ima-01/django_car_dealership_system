from apps.autoshows.models import Stock
from apps.common.services.base import BaseService


class AutoShowsStockService(BaseService):
    model = Stock
