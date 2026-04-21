import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .factories import UserFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(api_client):
    """Cliente autenticado con JWT válido."""
    user = UserFactory()
    response = api_client.post(
        reverse("users_api:login"),
        {"email": user.email, "password": "password123!"},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK, response.data
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client, user


class TestLoginEndpoint:
    def test_login_with_valid_credentials_returns_tokens(self, api_client):
        user = UserFactory(email="login@example.com")
        response = api_client.post(
            reverse("users_api:login"),
            {"email": user.email, "password": "password123!"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_with_invalid_password_returns_401(self, api_client):
        user = UserFactory()
        response = api_client.post(
            reverse("users_api:login"),
            {"email": user.email, "password": "wrong"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_with_nonexistent_email_returns_401(self, api_client):
        response = api_client.post(
            reverse("users_api:login"),
            {"email": "ghost@example.com", "password": "whatever"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestRefreshEndpoint:
    def test_refresh_with_valid_token_returns_new_access(self, api_client):
        user = UserFactory()
        login_resp = api_client.post(
            reverse("users_api:login"),
            {"email": user.email, "password": "password123!"},
            format="json",
        )
        refresh = login_resp.data["refresh"]

        response = api_client.post(
            reverse("users_api:refresh"),
            {"refresh": refresh},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data


class TestMeEndpoint:
    def test_me_unauthenticated_returns_401(self, api_client):
        response = api_client.get(reverse("users_api:me"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_authenticated_returns_user_data(self, auth_client):
        client, user = auth_client
        response = client.get(reverse("users_api:me"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(user.id)
        assert response.data["email"] == user.email

    def test_me_does_not_expose_password(self, auth_client):
        client, _ = auth_client
        response = client.get(reverse("users_api:me"))
        assert "password" not in response.data
        assert "is_staff" not in response.data
        assert "is_superuser" not in response.data

    def test_me_patch_updates_allowed_fields(self, auth_client):
        client, user = auth_client
        response = client.patch(
            reverse("users_api:me"),
            {"first_name": "Nuevo", "last_name": "Nombre"},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.first_name == "Nuevo"
        assert user.last_name == "Nombre"

    def test_me_patch_cannot_change_email(self, auth_client):
        client, user = auth_client
        original_email = user.email
        client.patch(
            reverse("users_api:me"),
            {"email": "hijacked@evil.com"},
            format="json",
        )
        user.refresh_from_db()
        assert user.email == original_email

    def test_me_patch_cannot_escalate_privileges(self, auth_client):
        client, user = auth_client
        assert user.is_staff is False
        assert user.is_superuser is False

        client.patch(
            reverse("users_api:me"),
            {"is_staff": True, "is_superuser": True},
            format="json",
        )
        user.refresh_from_db()
        assert user.is_staff is False
        assert user.is_superuser is False
