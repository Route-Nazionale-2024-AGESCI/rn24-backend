from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models

from common.abstract import CommonAbstractModel
from common.mixins import CMSPageLinkMixin
from people.models.person import Person

KINDERHEIM_NAMES = ["KINDEREHEIM 0-3", "KINDERHEIM 4-11", "KINGEREHEIM 12-15"]


class Squad(CMSPageLinkMixin, CommonAbstractModel):
    name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name="nome")
    description = models.TextField(verbose_name="descrizione", null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name="squads", blank=True, verbose_name="gruppi")
    page = models.ForeignKey(
        "cms.CMSPage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="pagina",
        help_text="la pagina CMS viene creata automaticamente al salvataggio",
    )

    @admin.display(description="n. persone")
    def people_count(self):
        return Person.objects.filter(squads=self).count()

    class Meta:
        verbose_name = "pattuglia"
        verbose_name_plural = "pattuglie"

    def __str__(self):
        return self.name
