from django.contrib import admin
from django.contrib.auth.models import Group
from django.db import models

from common.abstract import CommonAbstractModel
from people.models.person import Person


class Squad(CommonAbstractModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="nome")
    description = models.TextField(verbose_name="descrizione", null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name="squads", blank=True, verbose_name="gruppi")

    @admin.display(description="n. persone")
    def people_count(self):
        return Person.objects.filter(squads=self).count()

    class Meta:
        verbose_name = "pattuglia"
        verbose_name_plural = "pattuglie"

    def __str__(self):
        return self.name
