import pytest

from apps.autoshows.api.serializers.autoshows import AutoShowsSerializer
from apps.autoshows.models import AutoShow
from tests.autoshows.autoshows.factories import AutoShowFactory
from tests.base import BaseCRUDTest


@pytest.mark.django_db
class TestAutoShowsViews(BaseCRUDTest):
    model = AutoShow
    factory = AutoShowFactory
    serializer_class = AutoShowsSerializer
    url_list_name = "autoshows-list"
    url_detail_name = "autoshows-detail"

    @property
    def create_data(self):
        obj = AutoShowFactory.build()
        serializer = AutoShowsSerializer(obj)
        data = serializer.data
        data.pop("id", None)
        return data

    @property
    def update_data(self):
        return {"title": "New Title", "location": "US"}
