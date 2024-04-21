from django.db import transaction
from django.db.models import TextChoices
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from events.models import Event
from events.services.selectors import get_events_visible_to_person
from people.models import Person


class RegistrationErrors(TextChoices):
    NOT_VISIBLE = "iscrizione non consentita per questo evento"
    NOT_REQUIRED = "iscrizione non richiesta per questo evento"
    ALREADY_STARTED = "iscrizione non possibile: evento già iniziato"
    ALREADY_REGISTERED = "iscrizione non possibile: già registrato"
    FULL = "iscrizione non possibile: evento pieno"
    SAME_GROUP_LIMIT = "iscrizione non possibile: limite persone dello stesso gruppo raggiunto"
    REGISTRATION_NOT_OPEN_YET = "iscrizioni non ancora aperte"
    REGISTRATION_TIME_EXPIRED = "iscrizioni chiuse"


@transaction.atomic
def register_person_to_event(person: Person, event: Event):
    event = Event.objects.select_for_update("registered_persons").get(pk=event.pk)
    if event not in get_events_visible_to_person(person):
        raise ValidationError(RegistrationErrors.NOT_VISIBLE)
    if not event.is_registration_required:
        raise ValidationError(RegistrationErrors.NOT_REQUIRED)
    now = timezone.now()
    if now > event.starts_at:
        raise ValidationError(RegistrationErrors.ALREADY_STARTED)
    if event.registered_persons.filter(pk=person.pk).exists():
        raise ValidationError(RegistrationErrors.ALREADY_REGISTERED)
    if event.registration_limit and event.registered_persons.count() >= event.registration_limit:
        raise ValidationError(RegistrationErrors.FULL)
    if event.registration_limit_from_same_scout_group:
        if (
            event.registered_persons.filter(scout_group=person.scout_group).count()
            >= event.registration_limit_from_same_scout_group
        ):
            raise ValidationError(RegistrationErrors.SAME_GROUP_LIMIT)

    if event.registrations_open_at and now < event.registrations_open_at:
        raise ValidationError(RegistrationErrors.REGISTRATION_NOT_OPEN_YET)
    if event.registrations_close_at and now > event.registrations_close_at:
        raise ValidationError(RegistrationErrors.REGISTRATION_TIME_EXPIRED)

    event.registered_persons.add(person)
    event.save()


@transaction.atomic
def delete_personal_registration(person: Person, event: Event):
    event = Event.objects.select_for_update("registered_persons").get(pk=event.pk)
    if event.registered_persons.filter(pk=person.pk).exists():
        event.registered_persons.remove(person)
        event.save()