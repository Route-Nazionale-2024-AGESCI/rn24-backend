from django.db import transaction
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from people.models.person import Person
from people.models.squad import Squad


@receiver(m2m_changed, sender=Person.squads.through)
def person_squads_m2m__changed(sender, instance=None, action=None, **kwargs):
    if "post_" in action:
        with transaction.atomic():
            instance.set_permissions_from_squads()


@receiver(m2m_changed, sender=Squad.groups.through)
def squad_groups_m2m_changed(sender, instance=None, action=None, **kwargs):
    if "post_" in action:
        with transaction.atomic():
            for person in instance.members.all():
                person.set_permissions_from_squads()
