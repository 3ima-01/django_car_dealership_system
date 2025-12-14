import pytest
from rest_framework.test import APIClient

from apps.suppliers.models import Stock
from tests.base_nested import BaseNestedCRUDTest
from tests.cars.factories import CarFactory
from tests.suppliers.stock.factories import StockFactory
from tests.suppliers.suppliers.factories import SupplierFactory


@pytest.mark.django_db
class TestSupplierStockViews(BaseNestedCRUDTest):
    model = Stock
    factory = StockFactory
    parent_factory = SupplierFactory
    parent_field_name = "supplier"  # Stock.supplier → supplier_pk в URL

    url_list_name = "supplier-stock-list"
    url_detail_name = "supplier-stock-detail"

    @pytest.fixture
    def api_client(self):
        return APIClient()

    # Фабрика данных для создания — принимает parent (Supplier)
    def create_data_factory(self, supplier):
        car = CarFactory()
        return {
            "car": car.id,
            "quantity": 5,
            "price": "5000.00",
            # supplier НЕ передаём — он берётся из URL
        }

    def update_data_factory(self, obj):
        return {"quantity": obj.quantity + 10}
