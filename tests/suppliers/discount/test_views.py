from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.suppliers.models import Discount
from tests.base_nested import BaseNestedCRUDTest
from tests.cars.factories import CarFactory
from tests.suppliers.discount.factories import DiscountFactory
from tests.suppliers.suppliers.factories import SupplierFactory


@pytest.mark.django_db
class TestSupplierDiscountViews(BaseNestedCRUDTest):
    model = Discount
    factory = DiscountFactory
    parent_factory = SupplierFactory
    parent_field_name = "supplier"

    url_list_name = "supplier-discount-list"
    url_detail_name = "supplier-discount-detail"

    @pytest.fixture
    def api_client(self):
        return APIClient()

    def create_data_factory(self, supplier):
        cars = CarFactory.create_batch(2)
        car_ids = [car.id for car in cars]

        now = timezone.now()

        return {
            "name": "Test Discount",
            "description": "Test description",
            "discount_type": "percent",
            "value": "10.00",
            "cars": car_ids,
            "start_date": now.isoformat().replace("+00:00", "Z"),
            "end_date": (now + timedelta(days=7)).isoformat().replace("+00:00", "Z"),
        }

    def update_data_factory(self, obj):
        return {"value": obj.value + 10}
