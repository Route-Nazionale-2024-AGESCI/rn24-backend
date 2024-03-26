from django.db import models

from common.abstract import CommonAbstractModel

EVENT_KIND_CHOICES = (
    ("SGUARDI", "SGUARDI"),
    ("INCONTRI", "INCONTRI"),
    ("TRACCE", "TRACCE"),
    ("CONFRONTI", "CONFRONTI"),
)


class Event(CommonAbstractModel):
    name = models.CharField(max_length=255, db_index=True, verbose_name="nome")
    location = models.ForeignKey("maps.Location", on_delete=models.CASCADE, verbose_name="luogo")
    is_registration_required = models.BooleanField(
        default=True, verbose_name="registrazione richiesta?"
    )
    registration_limit = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="limite di iscrizioni"
    )
    registration_limit_from_same_scout_group = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="limite di iscrizioni dallo stesso groupo scout"
    )
    starts_at = models.DateTimeField(verbose_name="data inizio")
    ends_at = models.DateTimeField(verbose_name="data fine")
    registrations_open_at = models.DateTimeField(
        null=True, blank=True, verbose_name="data apertura iscrizioni"
    )
    registrations_close_at = models.DateTimeField(
        null=True, blank=True, verbose_name="data chiusura iscrizioni"
    )
    kind = models.CharField(max_length=255, choices=EVENT_KIND_CHOICES, verbose_name="modulo")

    class Meta:
        verbose_name = "evento"
        verbose_name_plural = "eventi"

    def __str__(self):
        return self.name
