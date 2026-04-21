import uuid

from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model that provides common fields and functionality for all models.
    Fields:
    - id: UUID v4 unique identifier.
    - created_at: DateTime field with auto-now-add functionality.
    -updated_at: DateTime field with auto-now functionality.
    Ordering:
    - created_at: Default ordering by creation date.
    - index DESC over created_at for faster queries.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="ID",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización",
    )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
        get_latest_by = "created_at"
        indexes = [
            models.Index(fields=["created_at"], name="%(class)s_created_idx"),
        ]
