import pytest

from apps.users.models import User


class TestUserManager:
    def test_create_user_normalizes_email(self):
        user = User.objects.create_user(email="Foo@EXAMPLE.COM", password="pass")
        assert user.email == "foo@example.com"  # la parte local NO se lowercaseá

    def test_create_user_requires_email(self):
        with pytest.raises(ValueError, match="email"):
            User.objects.create_user(email="", password="pass")

    def test_create_user_defaults(self):
        user = User.objects.create_user(email="u@x.com", password="pass")
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_superuser_sets_flags(self):
        admin = User.objects.create_superuser(email="a@x.com", password="pass")
        assert admin.is_staff is True
        assert admin.is_superuser is True

    def test_create_superuser_rejects_is_staff_false(self):
        with pytest.raises(ValueError, match="is_staff=True"):
            User.objects.create_superuser(email="a@x.com", password="pass", is_staff=False)

    def test_create_superuser_rejects_is_superuser_false(self):
        with pytest.raises(ValueError, match="is_superuser=True"):
            User.objects.create_superuser(email="a@x.com", password="pass", is_superuser=False)

    def test_password_is_hashed(self):
        user = User.objects.create_user(email="u@x.com", password="plain")
        assert user.password != "plain"
        assert user.check_password("plain") is True
