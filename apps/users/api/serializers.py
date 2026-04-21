from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Representación pública del user. Solo lectura."""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "second_last_name",
            "profile_picture",
            "is_active",
            "date_joined",
            "last_login",
        )
        read_only_fields = fields


class UserUpdateSerializer(serializers.ModelSerializer):
    """Campos que el propio user puede modificar vía PATCH /api/me/."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "second_last_name", "profile_picture")
