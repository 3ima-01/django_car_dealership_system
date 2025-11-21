from uuid import UUID

from apps.customers.models import Profiles


class ProfilesService:
    def __init__(self):
        self.model = Profiles

    def get(self, profile_id: UUID):
        return self.model.objects.filter(id=profile_id)
