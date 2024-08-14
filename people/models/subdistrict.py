from django.contrib import admin
from django.db import models

from common.abstract import CommonAbstractModel
from people.models.line import Line
from people.models.person import Person
from people.models.scout_group import ScoutGroup


class Subdistrict(CommonAbstractModel):
    name = models.CharField(max_length=255, verbose_name="nome")
    district = models.ForeignKey(
        "people.District", on_delete=models.CASCADE, verbose_name="sottocampo"
    )
    location = models.ForeignKey(
        "maps.Location", on_delete=models.CASCADE, null=True, blank=True, verbose_name="luogo"
    )

    @admin.display(description="n. file")
    def lines_count(self):
        return Line.objects.filter(subdistrict=self).count()

    @admin.display(description="n. gruppi scout")
    def scout_groups_count(self):
        return ScoutGroup.objects.filter(line__subdistrict=self).count()

    @admin.display(description="n. persone")
    def people_count(self):
        return Person.objects.filter(scout_group__line__subdistrict=self).count()

    class Meta:
        verbose_name = "contrada"
        verbose_name_plural = "contrade"

    def __str__(self):
        return f"{self.district.name} - {self.name}"
