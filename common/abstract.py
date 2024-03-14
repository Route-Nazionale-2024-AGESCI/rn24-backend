import uuid

from django.db import models
from django.utils.timezone import now

from common.managers import SoftDeletableManager


class CommonAbstractModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, editable=False, db_index=True)

    uuid = models.UUIDField(unique=True, editable=False, db_index=True, default=uuid.uuid4)

    deleted_at = models.DateTimeField(null=True, blank=True)

    objects_with_deleted = models.Manager()
    objects = SoftDeletableManager()

    def delete(self, using=None, soft=True, *args, **kwargs):
        if soft:
            self.deleted_at = now()
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)

    class Meta:
        abstract = True
