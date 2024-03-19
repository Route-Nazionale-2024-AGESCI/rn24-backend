from django.db import models

from common.abstract import CommonAbstractModel


class District(CommonAbstractModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="nome")

    class Meta:
        verbose_name = "sottocampo"
        verbose_name_plural = "sottocampi"

    def __str__(self):
        return self.name
