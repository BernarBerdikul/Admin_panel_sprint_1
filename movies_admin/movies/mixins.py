import uuid

from django.db import models


class UUIDMixin(models.Model):
    """Миксин для uuid первичного ключа"""

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    class Meta:
        abstract = True


class CreateTimeMixin(models.Model):
    """Миксин для времени создания"""

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class UpdateTimeMixin(CreateTimeMixin):
    """Миксин для времени создания и обновления"""

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
