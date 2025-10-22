from typing import Any
from uuid import UUID

from django.db.models import QuerySet

from apps.cars.models import Cars
from apps.cars.repositories.cars import CarsRepository


class CarsService:
    def __init__(self):
        self.repository = CarsRepository()

    def get_all_cars(self) -> QuerySet[Cars]:
        return self.repository.get_all()

    def get_car_by_id(self, car_id: UUID) -> Cars | None:
        car = self.repository.get_by_id(car_id)
        return car

    def get_car_by_id_or_404(self, car_id: UUID) -> Cars:
        return self.repository.get_by_id_or_404(car_id)

    def create_car(self, car_data: dict[str, Any]):
        return self.repository.create(car_data)

    def update_car(self, car_id: UUID, car_data: dict[str, Any]):
        return self.repository.update(car_id, car_data)

    def soft_delete_car(self, car_id: UUID):
        return self.repository.soft_delete(car_id)
