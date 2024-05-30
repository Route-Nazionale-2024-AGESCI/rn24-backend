import uuid

from django.db import models
from django.utils.timezone import now

from common.managers import SoftDeletableManager


class CommonAbstractModel(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, db_index=True, verbose_name="data di creazione"
    )
    updated_at = models.DateTimeField(
        auto_now=True, editable=False, db_index=True, verbose_name="data ultima modifica"
    )

    uuid = models.UUIDField(
        unique=True, editable=False, db_index=True, default=uuid.uuid4, verbose_name="UUID"
    )

    deleted_at = models.DateTimeField(
        null=True, blank=True, editable=False, db_index=True, verbose_name="data di cancellazione"
    )

    objects_with_deleted = models.Manager()
    objects = SoftDeletableManager()

    @classmethod
    def get_last_updated_timestamp(cls):
        last_updated = cls.objects.only("updated_at").order_by("-updated_at").first()
        if not last_updated:
            return now()
        return last_updated.updated_at

    def delete(self, using=None, soft=True, *args, **kwargs):
        if soft:
            self.deleted_at = now()
            self.save(using=using)
        else:
            return super().delete(using=using, *args, **kwargs)

    class Meta:
        abstract = True
