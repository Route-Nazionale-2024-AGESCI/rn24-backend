from django.contrib import admin
from django.db import models

from common.abstract import CommonAbstractModel
from people.models.scout_group import ScoutGroup


class District(CommonAbstractModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="nome")

    @admin.display(description="n. persone")
    def people_count(self):
        return self.subdistrict_set.count()

    @admin.display(description="n. contrade")
    def subdistricts_count(self):
        return self.subdistrict_set.count()

    @admin.display(description="n. gruppi scout")
    def scout_groups_count(self):
        return ScoutGroup.objects.filter(subdistrict__district=self).count()

    class Meta:
        verbose_name = "sottocampo"
        verbose_name_plural = "sottocampi"

    def __str__(self):
        return self.name
