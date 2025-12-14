from apps.common.services.base import BaseService
from apps.suppliers.models.stock import Stock


class SuppliersStockService(BaseService):
    model = Stock
