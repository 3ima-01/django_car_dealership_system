from typing import Any
from uuid import UUID

import pytest
from django.urls import reverse
from rest_framework import status


class BaseCRUDTest:
    model = None
    factory = None
    url_list_name = ""
    url_detail_name = ""
    create_data = dict[str, Any]
    update_data = dict[str, Any]
    serializer_class = None

    @classmethod
    def get_list_url(cls):
        return reverse(cls.url_list_name)

    @classmethod
    def get_detail_url(cls, pk):
        return reverse(cls.url_detail_name, kwargs={"pk": pk})

    @staticmethod
    def assert_uuid(data):
        assert "id" in data
        assert isinstance(UUID(data["id"]), UUID)

    @staticmethod
    def assert_fields(data, expected, fields=None):
        fields = fields or expected.keys()
        for field in fields:
            assert data[field] == expected[field], f"Field '{field}' mismatch"

    # --- List ---
    def test_list(self, api_client):
        self.factory.create_batch(3)
        response = api_client.get(self.get_list_url())
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_list_empty(self, api_client):
        response = api_client.get(self.get_list_url())
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    # --- Create ---
    def test_create(self, admin_client):
        response = admin_client.post(self.get_list_url(), self.create_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED

        obj = self.model.objects.get(pk=response.data["id"])

        serializer = self.serializer_class(obj)
        expected_data = serializer.data

        assert response.data == expected_data

    # --- Retrieve ---
    def test_retrieve(self, api_client):
        obj = self.factory()
        response = api_client.get(self.get_detail_url(obj.pk))
        assert response.status_code == status.HTTP_200_OK

        serializer = self.serializer_class(obj)
        expected_data = serializer.data

        assert response.data == expected_data

    # --- Partial ---
    def test_partial_update(self, admin_client):
        obj = self.factory()
        response = admin_client.patch(self.get_detail_url(obj.pk), self.update_data, format="json")
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_204_NO_CONTENT]

        obj.refresh_from_db()
        for field, value in self.update_data.items():
            assert getattr(obj, field) == value

    # --- Destroy ---
    def test_destroy(self, admin_client):
        obj = self.factory()
        response = admin_client.delete(self.get_detail_url(obj.pk))
        assert response.status_code == status.HTTP_204_NO_CONTENT

        obj.refresh_from_db()
        assert obj.is_active is False
