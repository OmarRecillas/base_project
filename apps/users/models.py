from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel

from .managers import UserManager


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    profile_picture = models.ImageField(
        upload_to="users/profile_pictures/%Y/%m/",
        blank=True,
        null=True,
        verbose_name=_("Foto de perfil"),
    )
    last_name = models.CharField(_("Primer apellido"), max_length=150, blank=True)
    second_last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("Segundo apellido"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta(BaseModel.Meta):
        db_table = "users"
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")

        def __str__(self):
            return self.email
