from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models

from common.abstract import CommonAbstractModel

User = get_user_model()


class Person(CommonAbstractModel):

    agesci_id = models.CharField(
        max_length=255, db_index=True, verbose_name="codice AGESCI", unique=True
    )

    user = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="utente"
    )

    first_name = models.CharField(db_index=True, max_length=255, verbose_name="nome")
    last_name = models.CharField(db_index=True, max_length=255, verbose_name="cognome")
    email = models.EmailField(db_index=True, unique=True, verbose_name="email")
    phone = models.CharField(max_length=255, blank=True, null=True, verbose_name="telefono")
    scout_group = models.ForeignKey(
        "people.ScoutGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="gruppo scout",
    )
    is_arrived = models.BooleanField(db_index=True, verbose_name="arrivato?", default=False)
    arrived_at = models.DateTimeField(verbose_name="data di arrivo", null=True, blank=True)

    squads = models.ManyToManyField(
        "people.Squad", related_name="members", blank=True, verbose_name="pattuglie"
    )

    @admin.display(description="pattuglie")
    def squads_list(self):
        return ", ".join([s.name for s in self.squads.all()])

    def set_permissions_from_squads(self):
        if not self.user:
            return
        groups = Group.objects.filter(squads__in=self.squads.all()).distinct()
        self.user.groups.clear()
        self.user.groups.add(*groups)
        if not self.user.is_superuser:
            self.user.is_staff = self.user.has_perm("people.is_staff")
            self.user.save(update_fields=["is_staff"])

    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "persone"
        permissions = (("is_staff", "Può accedere al backoffice"),)

    def __str__(self):
        return f"{self.first_name} {self.last_name} [{self.scout_group}]"
