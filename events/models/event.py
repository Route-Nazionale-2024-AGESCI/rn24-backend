from django.contrib import admin
from django.db import models, transaction
from django.utils.timezone import datetime, make_aware

from common.abstract import CommonAbstractModel
from common.mixins import CMSPageLinkMixin
from common.qr import QRCodeMixin
from events.models.event_registration import PersonEventRegistration
from people.models.scout_group import HAPPINESS_PATH_CHOICES

EVENT_KIND_CHOICES = (
    ("SGUARDI", "SGUARDI"),
    ("INCONTRI", "INCONTRI"),
    ("TRACCE", "TRACCE"),
    ("CONFRONTI", "CONFRONTI"),
    ("PASTI", "PASTI"),
    ("DOCCIA", "DOCCIA"),
    ("LOGISTICO", "LOGISTICO"),
    ("ALTRO", "ALTRO"),
)


class AnnotatedEventsManager(models.Manager):

    def with_registered_count(self):
        return self.annotate(persons_registration_count=models.Count("registered_persons"))


class Event(QRCodeMixin, CMSPageLinkMixin, CommonAbstractModel):
    """
    ogni COCA partecipa a 4 eventi di tipo di verso in 4 mezze giornate
    SGUARDI: eventi visibili a tutta la COCA, ogni capo si iscrive individualmente ad un evento
    CONFRONTI: eventi visibili a tutta la COCA, ogni capo si iscrive individualmente ad un evento
    TRACCE: la COCA viene iscritta a forza ad un evento specifico
    INCONTRI (alfieri): evento visibile a tutta la COCA, ma solo 2 alfieri per ogni gruppo devono iscriversi
    INCONTRI: il resto della COCA ha altri eventi visibili a tutta la COCA, a qualcuno ci si iscrive personalmente
    """

    name = models.CharField(max_length=255, db_index=True, verbose_name="nome")
    page = models.ForeignKey(
        "cms.CMSPage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="pagina",
        help_text="la pagina CMS viene creata automaticamente al salvataggio dell'evento",
    )
    location = models.ForeignKey("maps.Location", on_delete=models.CASCADE, verbose_name="luogo")
    is_registration_required = models.BooleanField(
        db_index=True, default=True, verbose_name="registrazione individuale abilitata?"
    )
    registration_limit = models.PositiveIntegerField(
        db_index=True, null=True, blank=True, verbose_name="limite di iscrizioni"
    )
    registration_limit_from_same_scout_group = models.PositiveIntegerField(
        db_index=True,
        null=True,
        blank=True,
        verbose_name="limite di iscrizioni dallo stesso groupo scout",
    )
    personal_registrations_count = models.PositiveIntegerField(
        db_index=True, default=0, verbose_name="numero di iscrizioni personali"
    )
    starts_at = models.DateTimeField(db_index=True, verbose_name="data inizio")
    ends_at = models.DateTimeField(db_index=True, verbose_name="data fine")
    registrations_open_at = models.DateTimeField(
        db_index=True, null=True, blank=True, verbose_name="data apertura iscrizioni"
    )
    registrations_close_at = models.DateTimeField(
        db_index=True, null=True, blank=True, verbose_name="data chiusura iscrizioni"
    )
    kind = models.CharField(
        db_index=True, max_length=255, choices=EVENT_KIND_CHOICES, verbose_name="modulo"
    )
    correlation_id = models.CharField(
        max_length=255,
        db_index=True,
        null=True,
        blank=True,
        verbose_name="id di correlazione accadimenti",
        help_text="deve essere uguale per tutti gli accandimenti dello stesso evento",
    )
    happiness_path = models.CharField(
        max_length=255,
        choices=HAPPINESS_PATH_CHOICES,
        null=True,
        blank=True,
        verbose_name="sentiero della felicità",
    )

    visibility_to_persons = models.ManyToManyField(
        "people.Person", through="events.PersonEventVisibility", related_name="visible_events"
    )
    visibility_to_scout_groups = models.ManyToManyField(
        "people.ScoutGroup",
        through="events.ScoutGroupEventVisibility",
        related_name="visible_events",
    )
    visibility_to_lines = models.ManyToManyField(
        "people.Line",
        through="events.LineEventVisibility",
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
    registered_lines = models.ManyToManyField(
        "people.Line",
        through="events.LineEventRegistration",
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

    objects_with_annotations = AnnotatedEventsManager()

    @classmethod
    def get_last_updated_timestamp(cls):
        event_timestamp = super().get_last_updated_timestamp()
        if PersonEventRegistration.objects.exists():
            personal_registration_timestamp = PersonEventRegistration.get_last_updated_timestamp()
        else:
            personal_registration_timestamp = make_aware(datetime(2000, 1, 1))
        return max(event_timestamp, personal_registration_timestamp)

    @admin.display(description="posti disponibili")
    def available_slots(self):
        if not self.registration_limit:
            return None
        return max(self.registration_limit - self.persons_registration_count(), 0)

    @admin.display(description="persone che vedono l'evento")
    def persons_visibility_count(self):
        from events.services.selectors import get_persons_visible_to_event

        return get_persons_visible_to_event(self).count()

    @admin.display(description="persone iscritte")
    def persons_registration_count(self):
        from events.services.selectors import get_persons_registered_to_event

        return get_persons_registered_to_event(self).count()

    def qr_payload(self):
        return f"E#{self.uuid}"

    def update_personal_registrations_count(self):
        with transaction.atomic():
            event = Event.objects.select_for_update().get(id=self.id)
            event.personal_registrations_count = event.registered_persons.count()
            event.save(update_fields=["personal_registrations_count"])

    class Meta:
        verbose_name = "evento"
        verbose_name_plural = "eventi"

    def __str__(self):
        return f"[{self.id}] {self.name}"
