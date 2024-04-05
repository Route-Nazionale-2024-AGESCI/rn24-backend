from django.contrib import admin
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

    visibility_to_persons = models.ManyToManyField(
        "people.Person", through="events.PersonEventVisibility", related_name="visible_events"
    )
    visibility_to_scout_groups = models.ManyToManyField(
        "people.ScoutGroup",
        through="events.ScoutGroupEventVisibility",
        related_name="visible_events",
    )
    visibility_to_subdistricts = models.ManyToManyField(
        "people.Subdistrict",
        through="events.SubdistrictEventVisibility",
        related_name="visible_events",
    )
    visibility_to_districts = models.ManyToManyField(
        "people.District",
        through="events.DistrictEventVisibility",
        related_name="visible_events",
    )
    visibility_to_squads = models.ManyToManyField(
        "people.Squad",
        through="events.SquadEventVisibility",
        related_name="visible_events",
    )

    registered_persons = models.ManyToManyField(
        "people.Person",
        through="events.PersonEventRegistration",
        related_name="registered_events",
    )
    registered_scout_groups = models.ManyToManyField(
        "people.ScoutGroup",
        through="events.ScoutGroupEventRegistration",
        related_name="registered_events",
    )
    registered_subdistricts = models.ManyToManyField(
        "people.Subdistrict",
        through="events.SubdistrictEventRegistration",
        related_name="registered_events",
    )
    registered_districts = models.ManyToManyField(
        "people.District",
        through="events.DistrictEventRegistration",
        related_name="registered_events",
    )
    registered_squads = models.ManyToManyField(
        "people.Squad",
        through="events.SquadEventRegistration",
        related_name="registered_events",
    )

    @admin.display(description="posti disponibili")
    def available_slots(self):
        return max(self.registration_limit - self.persons_registration_count(), 0)

    @admin.display(description="persone che vedono l'evento")
    def persons_visibility_count(self):
        from events.services.selectors import get_persons_visible_to_event

        return get_persons_visible_to_event(self).count()

    @admin.display(description="persone iscritte")
    def persons_registration_count(self):
        from events.services.selectors import get_persons_registered_to_event

        return get_persons_registered_to_event(self).count()

    class Meta:
        verbose_name = "evento"
        verbose_name_plural = "eventi"

    def __str__(self):
        return self.name
