import pytest

from apps.cars.api.serializers.cars import CarsSerializer
from apps.cars.models import Cars
from tests.base import BaseCRUDTest
from tests.cars.factories import CarFactory


@pytest.mark.django_db
class TestCarsViews(BaseCRUDTest):
    model = Cars
    factory = CarFactory
    serializer_class = CarsSerializer
    url_list_name = "cars-list"
    url_detail_name = "cars-detail"

    @property
    def create_data(self):
        obj = CarFactory.build()
        serializer = CarsSerializer(obj)
        data = serializer.data
        data.pop("id", None)
        return data

    @property
    def update_data(self):
        return {"brand": "Xiaomi", "horse_power": 999}
