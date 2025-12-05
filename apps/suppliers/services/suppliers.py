from typing import Any
from uuid import UUID

from django.db.models import QuerySet

from apps.suppliers.models import Suppliers
from apps.suppliers.repositories.suppliers import SuppliersRepository


class SuppliersService:
    def __init__(self):
        self.repository = SuppliersRepository()

    def get_all_suppliers(self) -> QuerySet[Suppliers]:
        return self.repository.get_all()

    def get_supplier_by_id_or_404(self, supplier_id: UUID) -> Suppliers:
        return self.repository.get_by_filter_or_404(id=supplier_id)

    def create_supplier(self, supplier_data: dict[str, Any]):
        return self.repository.create(supplier_data)

    def update_supplier(self, supplier_id: UUID, supplier_data: dict[str, Any]):
        return self.repository.update(supplier_id, supplier_data)

    def soft_delete_supplier(self, supplier_id: UUID):
        return self.repository.soft_delete(supplier_id)
