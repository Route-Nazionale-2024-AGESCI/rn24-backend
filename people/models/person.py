import base64

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from common.abstract import CommonAbstractModel
from common.crypto import sign_string
from common.qr import QRCodeMixin
from people.models.scout_group import ITALIAN_REGION_CHOICES

User = get_user_model()


class Person(QRCodeMixin, CommonAbstractModel):

    agesci_id = models.CharField(
        max_length=255,
        db_index=True,
        verbose_name="codice AGESCI",
        unique=True,
        null=True,
        blank=True,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="utente",
        help_text="se stai creando una persona lascia vuoto questo campo: un utente viene creato in automatico",
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

    def line_name(self):
        try:
            return self.scout_group.line.name
        except AttributeError:
            return ""

    def subdistrict_name(self):
        try:
            return self.scout_group.line.subdistrict.name
        except AttributeError:
            return ""

    def district_name(self):
        try:
            return self.scout_group.line.subdistrict.district.name
        except AttributeError:
            return ""

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

    def squad_list_string(self):
        return ", ".join([s.name for s in self.squads.all()])

    def qr_string(self):
        data = [
            "B",  # B=badge, P=page
            str(self.uuid),
            self.first_name,
            self.last_name,
            self.email,
            self.phone or "",
            self.scout_group.name if self.scout_group else "",
            self.region or "",
            self.line_name(),
            self.subdistrict_name(),
            self.district_name(),
            self.squad_list_string(),
        ]
        base_string = "#".join(data)
        return base64.b64encode(base_string.encode("utf-8")).decode("utf-8")

    def qr_string_with_signature(self):
        data = self.qr_string()
        return f"{data}#{sign_string(data)}"

    def qr_payload(self):
        return self.qr_string_with_signature()

    @admin.display(description="badge")
    def badge_url(self):
        HTML_url = reverse("badge-detail", kwargs={"uuid": self.uuid})
        PDF_url = reverse("badge-detail-pdf", kwargs={"uuid": self.uuid})
        return format_html(
            '<a href="{}" target="_blank">HTML</a> - <a href="{}" target="_blank">PDF</a>',
            HTML_url,
            PDF_url,
        )

    def is_staff(self):
        return self.user.has_perm("people.is_staff")

    def can_scan_qr(self):
        return self.user.has_perm("people.can_scan_qr")

    class Meta:
        verbose_name = "persona"
        verbose_name_plural = "persone"
        permissions = (
            ("is_staff", "Può accedere al backoffice"),
            ("can_scan_qr", "Può scansionare i badge"),
        )

    def __str__(self):
        group = f" [{self.scout_group.name}]" if self.scout_group else ""
        return f"[{self.agesci_id}] {self.first_name} {self.last_name}{group}"
