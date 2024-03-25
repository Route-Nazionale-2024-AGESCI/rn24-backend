from django.contrib import admin
from django.db import models

from common.abstract import CommonAbstractModel
from people.models.person import Person


class Subdistrict(CommonAbstractModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="nome")
    district = models.ForeignKey(
        "people.District", on_delete=models.CASCADE, verbose_name="sottocampo"
    )

    @admin.display(description="n. gruppi scout")
    def scout_groups_count(self):
        return self.scoutgroup_set.count()

    @admin.display(description="n. persone")
    def people_count(self):
        return Person.objects.filter(scout_group__subdistrict=self).count()

    class Meta:
        verbose_name = "contrada"
        verbose_name_plural = "contrade"

    def __str__(self):
        return self.name
