from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models

from common.abstract import CommonAbstractModel
from people.models.scout_group import ITALIAN_REGION_CHOICES

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
    email = models.EmailField(
        db_index=True, verbose_name="email", help_text="ricorda: purtroppo l'email non è univoca!"
    )
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

    birth_date = models.DateField(verbose_name="data di nascita", null=True, blank=True)
    gender = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=(("M", "Maschio"), ("F", "Femmina")),
        verbose_name="sesso",
    )
    training_level = models.CharField(
        max_length=255, verbose_name="livello di formazione", blank=True, null=True
    )
    address = models.CharField(max_length=255, verbose_name="indirizzo", blank=True, null=True)
    zip_code = models.CharField(max_length=255, verbose_name="CAP", blank=True, null=True)
    city = models.CharField(max_length=255, verbose_name="città", blank=True, null=True)
    province = models.CharField(max_length=255, verbose_name="provincia", blank=True, null=True)
    region = models.CharField(
        max_length=255,
        verbose_name="regione",
        blank=True,
        null=True,
        choices=ITALIAN_REGION_CHOICES,
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
            has_staff_permission = User.objects.get(pk=self.user.pk).has_perm("people.is_staff")
            self.user.is_staff = has_staff_permission
            self.user.save(update_fields=["is_staff"])

    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "persone"
        permissions = (("is_staff", "Può accedere al backoffice"),)

    def __str__(self):
        group = f" [{self.scout_group.name}]" if self.scout_group else ""
        return f"[{self.agesci_id}] {self.first_name} {self.last_name}{group}"
