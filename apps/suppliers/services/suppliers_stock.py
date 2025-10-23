from typing import Any
from uuid import UUID

from django.db.models import QuerySet

from apps.suppliers.models import SuppliersStock
from apps.suppliers.repositories.suppliers_stock import SuppliersStockRepository


class SuppliersStockService:
    def __init__(self):
        self.repository = SuppliersStockRepository()

    def get_supplier_stock(self, supplier_id: UUID) -> QuerySet[SuppliersStock]:
        return self.repository.get_supplier_stock(supplier_id)

    def add_car_to_supplier(self, supplier_stock_data: dict[str, Any]):
        return self.repository.create(supplier_stock_data)

    def update_supplier_car(self, supplier_stock_id: UUID, supplier_stock_data: dict[str, Any]):
        return self.repository.update(supplier_stock_id, supplier_stock_data)

    def delete_supplier_car(self, supplier_stock_id: UUID):
        return self.repository.soft_delete(supplier_stock_id)
