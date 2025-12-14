from apps.common.services.base import BaseService
from apps.customers.models import Profiles


class ProfilesService(BaseService):
    model = Profiles
