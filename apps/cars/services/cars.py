from apps.cars.models import Cars
from apps.common.services.base import BaseService


class CarsService(BaseService):
    model = Cars
