import base64

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

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

    # identity document
    identity_document_type = models.CharField(
        max_length=255, verbose_name="tipo documento", blank=True, null=True
    )
    identity_document_number = models.CharField(
        max_length=255, verbose_name="numero documento", blank=True, null=True
    )
    identity_document_issue_date = models.DateField(
        verbose_name="data rilascio documento", blank=True, null=True
    )
    identity_document_expiry_date = models.DateField(
        verbose_name="data scadenza documento", blank=True, null=True
    )

    # accessibility
    accessibility_has_wheelchair = models.BooleanField(
        default=False, db_index=True, verbose_name="sedia a rotelle?"
    )
    accessibility_has_caretaker_not_registered = models.BooleanField(
        default=False,
        verbose_name="accompagnatore?",
        help_text="viaggia con accompagnatore non iscritto?",
        db_index=True,
    )

    # sleeping
    sleeping_is_sleeping_in_tent = models.BooleanField(
        default=False, db_index=True, verbose_name="tenda?", help_text="dorme in tenda personale?"
    )
    sleeping_requests = models.TextField(
        null=True, blank=True, verbose_name="richieste per il pernotto"
    )
    sleeping_place = models.TextField(
        null=True,
        blank=True,
        verbose_name="Per motivi di disabilità/patologie ho bisogno di dormire:",
    )
    sleeping_requests_2 = models.TextField(
        null=True, blank=True, verbose_name="richieste per il pernotto (2)"
    )

    # food
    food_diet_needed = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="dieta",
        help_text="Allergie/intolleranze ad alimenti da segnalare.",
    )
    food_allergies = models.TextField(
        null=True, blank=True, verbose_name="Selezionare una o più allergie/intolleranze elencate:"
    )  # merged with "ALTRO"
    food_is_vegan = models.BooleanField(
        default=False, db_index=True, verbose_name="vegano?", help_text="Segui una dieta vegana?"
    )

    # transportation
    transportation_has_problems_moving_on_foot = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="spostamento a piedi?",
        help_text="Hai disabilità/patologie/età che non ti permettono di sostenere gli spostamenti a piedi previsti?",
    )
    transportation_need_transport = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Necessiti di un accompagnatore fornito dall'organizzazione durante l'evento?",
    )

    # health
    health_has_allergies = models.BooleanField(
        default=False, db_index=True, verbose_name="allergie?", help_text="Hai allergie accertate?"
    )
    health_allergies = models.TextField(
        null=True,
        blank=True,
        verbose_name="allergie",
    )
    health_has_movement_disorders = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="disturbi motori?",
        help_text="Sei affetto da disturbi motori?",
    )
    health_movement_disorders = models.TextField(
        null=True,
        blank=True,
        verbose_name="disturbi motori",
    )
    health_has_patologies = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="patologie?",
        help_text="Sei affetto da patologie cardiovascolari/respiratorie/neurologiche?",
    )
    health_patologies = models.TextField(
        null=True,
        blank=True,
        verbose_name="patologie accertate",
    )
    is_available_for_extra_service = models.BooleanField(
        default=False, db_index=True, verbose_name="disponibile per servizio extra?"
    )

    notes = models.TextField(null=True, blank=True, verbose_name="note")

    SENSIBLE_FIELDS = [
        "accessibility_has_wheelchair",
        "accessibility_has_caretaker_not_registered",
        "sleeping_is_sleeping_in_tent",
        "sleeping_requests",
        "sleeping_place",
        "sleeping_requests_2",
        "food_diet_needed",
        "food_allergies",
        "food_is_vegan",
        "transportation_has_problems_moving_on_foot",
        "transportation_need_transport",
        "health_has_allergies",
        "health_allergies",
        "health_has_movement_disorders",
        "health_movement_disorders",
        "health_has_patologies",
        "health_patologies",
    ]

    @admin.display(description="pattuglie")
    def squads_list(self):
        return ", ".join([s.name for s in self.squads.all()])

    @admin.display(description="nome")
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @admin.display(description="fila")
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

    @admin.display(description="Gruppo scout")
    def scout_group_link(self):
        if not self.scout_group:
            return None
        url = reverse("admin:people_scoutgroup_change", args=[self.scout_group.id])
        link = f'<a href="{url}">{self.scout_group.name}</a>'
        return mark_safe(link)

    @admin.display(description="Persona")
    def person_admin_link(self):
        url = reverse("admin:people_person_change", args=[self.id])
        link = f'<a href="{url}">{self}</a>'
        return mark_safe(link)

    @admin.display(description="Dati sensibili")
    def sensible_data_admin_link(self):
        url = reverse("admin:people_sensibledata_change", args=[self.id])
        link = f'<a href="{url}">{self}</a>'
        return mark_safe(link)

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

    def save(self, *args, **kwargs):
        if self.agesci_id == "":
            self.agesci_id = None
        super().save(*args, **kwargs)

    def __str__(self):
        group = f" [{self.scout_group.name}]" if self.scout_group else ""
        agesci_id = f"[{self.agesci_id}] " if self.agesci_id else ""
        return f"{agesci_id}{self.first_name} {self.last_name}{group}"
