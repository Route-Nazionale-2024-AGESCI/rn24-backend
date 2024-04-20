from django.contrib.gis.db import models

from common.abstract import CommonAbstractModel


class Location(CommonAbstractModel):
    name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name="nome")
    coords = models.PointField(verbose_name="coordinate")
    polygon = models.PolygonField(null=True, blank=True, verbose_name="poligono")

    class Meta:
        verbose_name = "luogo"
        verbose_name_plural = "luoghi"

    def __str__(self):
        return self.name
