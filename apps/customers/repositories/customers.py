from apps.common.repositories import BaseRepository
from apps.customers.models import Customers


class CustomersRepository(BaseRepository[Customers]):
    model = Customers
