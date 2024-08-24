from django.db import transaction
from django.utils import timezone

from people.models.person import Person
from people.models.scout_group import ScoutGroup


@transaction.atomic
def mark_check_in(queryset, direction, user):
    if direction not in ["ENTRATA", "USCITA"]:
        return
    is_arrived = direction == "ENTRATA"
    now = timezone.now()
    locked_qs = Person.objects.select_for_update().filter(pk__in=queryset)
    locked_qs.exclude(is_arrived=is_arrived).update(is_arrived=is_arrived, arrived_at=now)
    scout_group_qs = ScoutGroup.objects.filter(person__in=locked_qs).distinct()
    if direction == "ENTRATA":
        scout_group_qs.exclude(is_arrived=is_arrived).update(is_arrived=is_arrived, arrived_at=now)
    if direction == "USCITA":
        for scout_group in scout_group_qs:
            if scout_group.person_set.filter(is_arrived=True).exclude(id__in=locked_qs).exists():
                continue
            scout_group.is_arrived = False
            scout_group.save()
    for person in locked_qs:
        person.personcheckin_set.create(direction=direction, user=user)
