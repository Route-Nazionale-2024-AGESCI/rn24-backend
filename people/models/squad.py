from django.db import models

from common.abstract import CommonAbstractModel


class Squad(CommonAbstractModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="nome")
    description = models.TextField(verbose_name="descrizione", null=True, blank=True)

    class Meta:
        verbose_name = "pattuglia"
        verbose_name_plural = "pattuglie"

    def __str__(self):
        return self.name
