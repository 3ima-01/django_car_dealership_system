import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        email="admin@test.com",
        password="password",
        first_name="A",
        last_name="B",
        is_staff=True,
        is_active=True,
    )


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def api_client():
    return APIClient()
