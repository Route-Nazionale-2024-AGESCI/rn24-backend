from django.db import models

from common.abstract import CommonAbstractModel


class Subdistrict(CommonAbstractModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="nome")
    district = models.ForeignKey(
        "people.District", on_delete=models.CASCADE, verbose_name="sottocampo"
    )

    class Meta:
        verbose_name = "contrada"
        verbose_name_plural = "contrade"

    def __str__(self):
        return self.name
