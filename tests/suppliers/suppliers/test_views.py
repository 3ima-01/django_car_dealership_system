import pytest

from apps.suppliers.api.serializers.suppliers import SuppliersSerializer
from apps.suppliers.models import Supplier
from tests.base import BaseCRUDTest
from tests.suppliers.suppliers.factories import SupplierFactory


@pytest.mark.django_db
class TestSuppliersViews(BaseCRUDTest):
    model = Supplier
    factory = SupplierFactory
    serializer_class = SuppliersSerializer
    url_list_name = "suppliers-list"
    url_detail_name = "suppliers-detail"

    @property
    def create_data(self):
        obj = SupplierFactory.build()
        serializer = SuppliersSerializer(obj)
        data = serializer.data
        data.pop("id", None)
        return data

    @property
    def update_data(self):
        return {"title": "New Title", "year": 2000}
