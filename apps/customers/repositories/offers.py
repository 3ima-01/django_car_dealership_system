from decimal import Decimal
from uuid import UUID

from apps.common.repositories import BaseRepository
from apps.customers.models import Offers


class OffersRepository(BaseRepository[Offers]):
    model = Offers

    def create(
        self,
        customer: UUID,
        model: str,
        max_price: Decimal,
    ):
        return self.model._default_manager.create(
            customer=customer,
            model=model,
            max_price=max_price,
        )
