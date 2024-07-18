import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction
from django.db.models.signals import m2m_changed, post_delete, post_save, pre_save
from django.dispatch import receiver

from cms.models.page import CMSPage
from events.models.event import Event
from events.models.event_registration import (
    DistrictEventRegistration,
    LineEventRegistration,
    PersonEventRegistration,
    SquadEventRegistration,
    SubdistrictEventRegistration,
)
from events.models.event_visibility import (
    DistrictEventVisibility,
    LineEventVisibility,
    PersonEventVisibility,
    ScoutGroupEventVisibility,
    SquadEventVisibility,
    SubdistrictEventVisibility,
)
from maps.models.location import Location
from people.models.district import District
from people.models.line import Line
from people.models.person import Person
from people.models.scout_group import ScoutGroup
from people.models.squad import Squad
from people.models.subdistrict import Subdistrict

User = get_user_model()

logger = logging.getLogger(__name__)


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


# invalidate cache
@receiver([post_save, post_delete], sender=Person)
@receiver([post_save, post_delete], sender=User)
@receiver([post_save, post_delete], sender=Squad)
@receiver([post_save, post_delete], sender=ScoutGroup)
@receiver([post_save, post_delete], sender=Line)
@receiver([post_save, post_delete], sender=Subdistrict)
@receiver([post_save, post_delete], sender=District)
@receiver([post_save, post_delete], sender=CMSPage)
@receiver([post_save, post_delete], sender=Location)
@receiver([post_save, post_delete], sender=Event)
@receiver([post_save, post_delete], sender=SquadEventVisibility)
@receiver([post_save, post_delete], sender=LineEventVisibility)
@receiver([post_save, post_delete], sender=SubdistrictEventVisibility)
@receiver([post_save, post_delete], sender=DistrictEventVisibility)
@receiver([post_save, post_delete], sender=ScoutGroupEventVisibility)
@receiver([post_save, post_delete], sender=PersonEventVisibility)
@receiver([post_save, post_delete], sender=SquadEventRegistration)
@receiver([post_save, post_delete], sender=PersonEventRegistration)
@receiver([post_save, post_delete], sender=LineEventRegistration)
@receiver([post_save, post_delete], sender=SubdistrictEventRegistration)
@receiver([post_save, post_delete], sender=DistrictEventRegistration)
@receiver([post_save, post_delete], sender=SquadEventRegistration)
def invalidate_cache(sender, instance=None, **kwargs):
    if not settings.DEBUG:
        logger.info("Invalidating cache for %s: %s", sender, instance)
        cache.clear()


@receiver(pre_save, sender=Squad)
def create_squad_cmspage(sender, instance=None, created=False, **kwargs):
    if not instance.page:
        from cms.models import CMSPage

        try:
            events_page = CMSPage.objects.get(title="Pattuglie")
            page = CMSPage(title=instance.name)
            events_page.add_child(instance=page)
            instance.page = page
        except CMSPage.DoesNotExist:
            logger.error("Page 'Pattuglie' not found")
    elif instance.page.title != instance.name:
        instance.page.title = instance.name
        instance.page.save()
