from apps.common.services.base import BaseService
from apps.suppliers.models.supplier import Supplier


class SuppliersService(BaseService):
    model = Supplier
