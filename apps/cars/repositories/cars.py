from apps.cars.models import Cars
from apps.common.repositories import BaseRepository


class CarsRepository(BaseRepository[Cars]):
    model = Cars
