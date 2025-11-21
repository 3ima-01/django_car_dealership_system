from apps.common.repositories import BaseRepository
from apps.suppliers.models import Suppliers


class SuppliersRepository(BaseRepository[Suppliers]):
    model = Suppliers
