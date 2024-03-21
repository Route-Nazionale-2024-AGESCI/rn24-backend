from django.contrib import admin
from django.db import models

from common.abstract import CommonAbstractModel


class Subdistrict(CommonAbstractModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="nome")
    district = models.ForeignKey(
        "people.District", on_delete=models.CASCADE, verbose_name="sottocampo"
    )

    @admin.display(description="n. gruppi scout")
    def scout_groups_count(self):
        return self.scoutgroup_set.count()

    class Meta:
        verbose_name = "contrada"
        verbose_name_plural = "contrade"

    def __str__(self):
        return self.name
