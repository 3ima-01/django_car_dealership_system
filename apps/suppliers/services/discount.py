from typing import Any
from uuid import UUID

from apps.common.services.base import BaseService
from apps.suppliers.models.discount import Discount


class DiscountService(BaseService):
    model = Discount

    def create(self, supplier_id: UUID, data: dict[str, Any]):
        return self.model.objects.create_discount(supplier_id, data)
