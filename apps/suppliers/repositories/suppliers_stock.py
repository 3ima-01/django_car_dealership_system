from uuid import UUID

from apps.common.repositories import BaseRepository
from apps.suppliers.models import SuppliersStock


class SuppliersStockRepository(BaseRepository[SuppliersStock]):
    model = SuppliersStock

    def get_supplier_stock(self, supplier_id: UUID):
        return self.model.objects.filter(supplier_id=supplier_id, is_active=True)
