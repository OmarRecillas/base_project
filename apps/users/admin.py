from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ("-created_at",)
    list_display = ("email", "first_name", "last_name", "is_staff", "created_at")
    search_fields = ("email", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Información personal"),
            {
                "fields": ("first_name", "last_name", "second_last_name", "profile_picture"),
            },
        ),
        (
            _("Permisos"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Fechas importantes"),
            {
                "fields": ("last_login", "date_joined", "created_at", "updated_at"),
            },
        ),
    )
    readonly_fields = ("id", "last_login", "date_joined", "created_at", "updated_at")

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
