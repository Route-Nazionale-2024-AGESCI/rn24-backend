import math

from django.contrib import admin
from django.db import models

from common.abstract import CommonAbstractModel
from people.models.person import Person


class Line(CommonAbstractModel):
    name = models.CharField(max_length=255, verbose_name="nome")
    subdistrict = models.ForeignKey(
        "people.Subdistrict", on_delete=models.CASCADE, verbose_name="contrada"
    )
    location = models.ForeignKey("maps.Location", on_delete=models.CASCADE, verbose_name="luogo")

    square_meters = models.DecimalField(
        null=True, blank=True, verbose_name="metri quadri", max_digits=10, decimal_places=2
    )
    tent_slots = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="posti tenda")

    @admin.display(description="n. gruppi scout")
    def scout_groups_count(self):
        return self.scoutgroup_set.count()

    @admin.display(description="n. persone")
    def people_count(self):
        return Person.objects.filter(scout_group__line=self).count()

    @admin.display(description="numero tende stimato")
    def tents_count_estimate(self):
        return math.ceil(self.people_count() / 3)

    class Meta:
        verbose_name = "fila"
        verbose_name_plural = "file"

    def __str__(self):
        return f"{self.subdistrict.district.name} - {self.subdistrict.name} - {self.name}"
