from uuid import UUID

import pytest
from django.urls import reverse
from rest_framework import status


class BaseNestedCRUDTest:
    """
    Base class for CRUD tests of nested resources (drf-nested-routers).
    """

    # Child data
    model = None
    factory = None
    # Parent data
    parent_factory = None
    parent_field_name = None

    url_list_name = ""  # "supplier-stock-list"
    url_detail_name = ""  # "supplier-stock-detail"

    def get_list_url(self, parent):
        return reverse(self.url_list_name, kwargs={f"{self.parent_field_name}_pk": parent.pk})

    def get_detail_url(self, obj):
        return reverse(
            self.url_detail_name,
            kwargs={
                f"{self.parent_field_name}_pk": getattr(obj, self.parent_field_name).pk,
                "pk": obj.pk,
            },
        )

    # --- Utils ---
    @staticmethod
    def assert_uuid(data):
        assert "id" in data, "'id' missing"
        try:
            uuid_obj = UUID(data["id"])
        except ValueError:
            pytest.fail(f"Invalid UUID: {data['id']}")
        assert isinstance(uuid_obj, UUID)

    @staticmethod
    def _normalize_uuid(value):
        """Convert UUID/model/str → lowercase UUID string, or return unchanged."""
        if not value:
            return value
        try:
            return str(UUID(str(value))).lower()
        except (ValueError, TypeError):
            return value

    @staticmethod
    def assert_fields(data, expected, fields=None):
        fields = fields or expected.keys()
        for field in fields:
            assert field in data, f"Field '{field}' missing"
            actual = data[field]
            expected_val = expected[field]

            actual = BaseNestedCRUDTest._normalize_uuid(actual)
            expected_val = BaseNestedCRUDTest._normalize_uuid(expected_val)

            if not isinstance(actual, list):
                assert actual == expected_val, f"Mismatch in '{field}': {actual} != {expected_val}"
            else:
                assert set(actual) == set(expected_val), f"Mismatch in '{field}': {actual} != {expected_val}"

    @pytest.fixture
    def parent(self):
        return self.parent_factory()

    @pytest.fixture
    def child(self, parent):
        return self.factory(**{self.parent_field_name: parent})

    # --- Tests ---
    def test_list(self, api_client, parent):
        self.factory.create_batch(3, **{self.parent_field_name: parent})
        url = self.get_list_url(parent)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_list_empty(self, api_client, parent):
        url = self.get_list_url(parent)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_create(self, admin_client, parent):
        data = self.create_data_factory(parent)
        url = self.get_list_url(parent)
        response = admin_client.post(url, data, format="json")

        if response.status_code != status.HTTP_201_CREATED:
            pytest.fail(
                f"Create failed.\nURL: {url}\nData: {data}\nStatus: {response.status_code}\nResponse: {response.data}"
            )

        assert response.status_code == status.HTTP_201_CREATED
        self.assert_uuid(response.data)

        obj = self.model.objects.get(pk=response.data["id"])
        assert getattr(obj, self.parent_field_name) == parent

        expected_for_check = {k: v for k, v in data.items() if k != self.parent_field_name}
        self.assert_fields(response.data, expected_for_check)

    def test_retrieve(self, api_client, child):
        url = self.get_detail_url(child)
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(child.pk)

    def test_partial_update(self, admin_client, child):
        update_data = self.update_data_factory(child)
        url = self.get_detail_url(child)
        response = admin_client.patch(url, update_data, format="json")
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

        child.refresh_from_db()
        for field, value in update_data.items():
            assert getattr(child, field) == value

    def test_destroy(self, admin_client, child):
        url = self.get_detail_url(child)
        response = admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

        child.refresh_from_db()
        if hasattr(child, "is_active"):
            assert child.is_active is False
