from django.contrib.gis.db import models

from common.abstract import CommonAbstractModel


class Location(CommonAbstractModel):
    name = models.CharField(max_length=255, db_index=True, verbose_name="nome")
    description = models.TextField(blank=True, null=True, verbose_name="descrizione")
    is_public = models.BooleanField(
        default=False,
        verbose_name="pubblico?",
        help_text="se attivo, viene mostrato sempre sulla mappa",
    )
    category = models.ForeignKey(
        "maps.LocationCategory",
        on_delete=models.CASCADE,
        verbose_name="categoria",
        null=True,
        blank=True,
    )
    coords = models.PointField(verbose_name="coordinate")
    path = models.LineStringField(null=True, blank=True, verbose_name="linea")
    polygon = models.PolygonField(null=True, blank=True, verbose_name="poligono")

    class Meta:
        verbose_name = "luogo"
        verbose_name_plural = "luoghi"

    def __str__(self):
        return self.name
