from django.db import models


class SoftDeletableManager(models.Manager):
    def get_queryset(self):
        super().get_queryset().filter(deleted_at__isnull=True)
