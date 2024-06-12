from django.contrib import admin
from django.db import models
from django.utils.html import format_html

from common.abstract import CommonAbstractModel


class LocationCategory(CommonAbstractModel):
    name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name="nome")
    icon = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="icona",
        help_text="scegli il codice icona di font awesome https://fontawesome.com/icons",
    )

    @admin.display(description="icona")
    def icon_html(self):
        return format_html('<i class="fa-solid {}"></i>', self.icon)

    class Meta:
        verbose_name = "categoria luogo"
        verbose_name_plural = "categorie luogo"

    def __str__(self) -> str:
        return self.name
