from uuid import UUID

from apps.accounts.models import Customers
from apps.common.repositories import BaseRepository


class AccountsRepository(BaseRepository[Customers]):
    model = Customers

    def get_by_email(self, email: str):
        try:
            return self.model.objects.get(email=email, is_active=True)
        except self.model.DoesNotExist:
            return None

    def verify_by_id(self, id: UUID):
        return self.model.objects.filter(pk=id, is_active=True).update(is_verified=True)
