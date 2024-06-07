from django.db.models import Q, Value

from events.models.event import Event
from people.models.person import Person


def get_events_visible_to_person(person: Person):
    return Event.objects.filter(
        Q(visibility_to_persons=person)
        | Q(visibility_to_scout_groups=person.scout_group)
        | Q(visibility_to_lines=person.scout_group.line)
        | Q(visibility_to_subdistricts=person.scout_group.line.subdistrict)
        | Q(visibility_to_districts=person.scout_group.line.subdistrict.district)
        | Q(visibility_to_squads__in=person.squads.all())
    )


def get_events_registered_to_person(person: Person):
    personal_events = Event.objects.filter(registered_persons=person).annotate(
        is_personal=Value(True)
    )
    passive_events = Event.objects.filter(
        Q(registered_scout_groups=person.scout_group)
        | Q(registered_lines=person.scout_group.line)
        | Q(registered_subdistricts=person.scout_group.line.subdistrict)
        | Q(registered_districts=person.scout_group.line.subdistrict.district)
        | Q(registered_squads__in=person.squads.all())
    ).annotate(is_personal=Value(False))
    return personal_events.union(passive_events)


def get_persons_visible_to_event(event: Event):
    return Person.objects.filter(
        Q(visible_events=event)
        | Q(scout_group__visible_events=event)
        | Q(scout_group__line__visible_events=event)
        | Q(scout_group__line__subdistrict__visible_events=event)
        | Q(scout_group__line__subdistrict__district__visible_events=event)
        | Q(squads__visible_events=event)
    ).distinct()


def get_persons_registered_to_event(event: Event):
    return Person.objects.filter(
        Q(registered_events=event)
        | Q(scout_group__registered_events=event)
        | Q(scout_group__line__registered_events=event)
        | Q(scout_group__line__subdistrict__registered_events=event)
        | Q(scout_group__line__subdistrict__district__registered_events=event)
        | Q(squads__registered_events=event)
    ).distinct()
