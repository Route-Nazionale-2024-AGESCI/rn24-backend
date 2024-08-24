import math

from django.contrib import admin
from django.db import models

from common.abstract import CommonAbstractModel

HAPPINESS_PATH_CHOICES = (
    ("Felici di accogliere", "Felici di accogliere"),
    ("Felici di vivere una vita giusta", "Felici di vivere una vita giusta"),
    ("Felici di prendersi cura e custodire", "Felici di prendersi cura e custodire"),
    ("Felici di generare speranza", "Felici di generare speranza"),
    ("Felici di fare esperienza di Dio", "Felici di fare esperienza di Dio"),
    ("Felici di essere appassionati", "Felici di essere appassionati"),
    ("Felici di lavorare per la pace", "Felici di lavorare per la pace"),
    ("Felici di essere profeti in un mondo nuovo", "Felici di essere profeti in un mondo nuovo"),
)

ITALIAN_REGION_CHOICES = (
    ("ABRUZZO", "Abruzzo"),
    ("BASILICATA", "Basilicata"),
    ("CALABRIA", "Calabria"),
    ("CAMPANIA", "Campania"),
    ("EMILIA ROMAGNA", "Emilia-Romagna"),
    ("FRIULI VENEZIA GIULIA", "Friuli-Venezia Giulia"),
    ("LAZIO", "Lazio"),
    ("LIGURIA", "Liguria"),
    ("LOMBARDIA", "Lombardia"),
    ("MARCHE", "Marche"),
    ("MOLISE", "Molise"),
    ("PIEMONTE", "Piemonte"),
    ("PUGLIA", "Puglia"),
    ("SARDEGNA", "Sardegna"),
    ("SICILIA", "Sicilia"),
    ("TOSCANA", "Toscana"),
    ("TRENTINO ALTO ADIGE", "Trentino-Alto Adige"),
    ("UMBRIA", "Umbria"),
    ("VALLE D'AOSTA", "Valle d'Aosta"),
    ("VENETO", "Veneto"),
)


class ScoutGroup(CommonAbstractModel):
    agesci_id = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="codice AGESCI"
    )
    name = models.CharField(max_length=255, db_index=True, unique=True, verbose_name="nome")
    zone = models.CharField(max_length=255, verbose_name="zona")
    region = models.CharField(
        max_length=255, choices=ITALIAN_REGION_CHOICES, verbose_name="regione"
    )
    line = models.ForeignKey(
        "people.Line",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="fila",
    )
    happiness_path = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        choices=HAPPINESS_PATH_CHOICES,
        verbose_name="sentiero della felicità",
    )
    is_arrived = models.BooleanField(
        db_index=True, verbose_name="almeno un presente?", default=False
    )
    arrived_at = models.DateTimeField(verbose_name="data di arrivo", null=True, blank=True)

    arrival_date = models.DateTimeField(verbose_name="data di arrivo", null=True, blank=True)
    departure_date = models.DateTimeField(verbose_name="data di partenza", null=True, blank=True)
    has_problems_with_payments = models.BooleanField(
        verbose_name="problemi pagamento?", default=False
    )
    problems_with_payments = models.TextField(
        verbose_name="problemi pagamento", null=True, blank=True
    )
    notes = models.TextField(verbose_name="note", null=True, blank=True)

    @admin.display(description="n. persone")
    def people_count(self):
        return self.person_set.all().count()

    @admin.display(description="sottocampo")
    def district(self):
        return self.line.subdistrict.district

    @admin.display(description="contrada")
    def subdistrict(self):
        return self.line.subdistrict

    @admin.display(description="numbero bambini")
    def children_count(self):
        from people.models.squad import KINDERHEIM_NAMES

        return self.person_set.filter(squads__name__in=KINDERHEIM_NAMES).count()

    @admin.display(description="numero tende")
    def tents_count(self):
        return math.ceil(self.people_count() / 3)

    class Meta:
        verbose_name = "gruppo scout"
        verbose_name_plural = "gruppi scout"

    def __str__(self):
        return self.name
