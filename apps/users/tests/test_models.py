import uuid

import pytest

from .factories import UserFactory


class TestUserModel:
    def test_str_returns_email(self):
        user = UserFactory(email="test@example.com")
        assert str(user) == "test@example.com"

    def test_pk_is_uuid(self):
        user = UserFactory()
        assert isinstance(user.id, uuid.UUID)

    def test_has_timestamps(self):
        user = UserFactory()
        assert user.created_at is not None
        assert user.updated_at is not None
        assert user.updated_at >= user.created_at

    def test_default_ordering_newest_first(self):
        from apps.users.models import User

        u1 = UserFactory()
        u2 = UserFactory()
        u3 = UserFactory()

        ordered = list(User.objects.all())
        assert ordered == [u3, u2, u1]

    def test_email_is_unique(self):
        from django.db import IntegrityError

        UserFactory(email="dup@example.com")
        with pytest.raises(IntegrityError):
            UserFactory(email="dup@example.com")._meta.model.objects.create(email="dup@example.com")
