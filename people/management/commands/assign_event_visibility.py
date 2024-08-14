from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from events.models.event import Event
from people.models.district import District

User = get_user_model()


class Command(BaseCommand):
    help = "assegna la visibilità degli eventi in base ai moduli ad ogni sottocampo"

    """
    ROSSO 23 Mattina TRACCE 23 -  Pomeriggio SGUARDI - 24 Mattina INCONTRI - 24 Pomeriggio CONFRONTI
    VIOLA 23 Mattina SGUARDI - 23 Pomeriggio TRACCE - 24 Mattina CONFRONTI - 24 Pomeriggio INCONTRI
    VERDE 23 Mattina INCONTRI - 23 Pomeriggio CONFRONTI -  24 Mattina TRACCE - 24  Pomeriggio SGUARDI
    GIALLO 23 Mattina CONFRONTI - 23 Pomeriggio INCONTRI - 24 Mattina SGUARDI - 24 Pomeriggio TRACCE
    """

    def handle(self, *args, **options):
        with transaction.atomic():

            rosso = District.objects.get(name="ROSSO")
            viola = District.objects.get(name="VIOLA")
            verde = District.objects.get(name="VERDE")
            giallo = District.objects.get(name="GIALLO")

            ven_mat = dict(
                starts_at__gte="2024-08-23 06:00",
                ends_at__lte="2024-08-23 13:01",
            )
            ven_pom = dict(
                starts_at__gte="2024-08-23 13:01",
                ends_at__lte="2024-08-23 22:00",
            )
            sab_mat = dict(
                starts_at__gte="2024-08-24 06:00",
                ends_at__lte="2024-08-24 13:01",
            )
            sab_pom = dict(
                starts_at__gte="2024-08-24 13:01",
                ends_at__lte="2024-08-24 22:00",
            )

            sguardi_ven_mat = Event.objects.filter(**ven_mat, kind="SGUARDI")
            sguardi_ven_pom = Event.objects.filter(**ven_pom, kind="SGUARDI")
            sguardi_sab_mat = Event.objects.filter(**sab_mat, kind="SGUARDI")
            sguardi_sab_pom = Event.objects.filter(**sab_pom, kind="SGUARDI")

            assert (
                sguardi_ven_mat.count()
                + sguardi_ven_pom.count()
                + sguardi_sab_mat.count()
                + sguardi_sab_pom.count()
                == Event.objects.filter(kind="SGUARDI").count()
            )

            confronti_ven_mat = Event.objects.filter(**ven_mat, kind="CONFRONTI")
            confronti_ven_pom = Event.objects.filter(**ven_pom, kind="CONFRONTI")
            confronti_sab_mat = Event.objects.filter(**sab_mat, kind="CONFRONTI")
            confronti_sab_pom = Event.objects.filter(**sab_pom, kind="CONFRONTI")

            assert (
                confronti_ven_mat.count()
                + confronti_ven_pom.count()
                + confronti_sab_mat.count()
                + confronti_sab_pom.count()
                == Event.objects.filter(kind="CONFRONTI").count()
            )

            incontri_ven_mat = Event.objects.filter(**ven_mat, kind="INCONTRI").exclude(
                registration_limit_from_same_scout_group__gte=0
            )
            incontri_ven_pom = Event.objects.filter(**ven_pom, kind="INCONTRI").exclude(
                registration_limit_from_same_scout_group__gte=0
            )
            incontri_sab_mat = Event.objects.filter(**sab_mat, kind="INCONTRI").exclude(
                registration_limit_from_same_scout_group__gte=0
            )
            incontri_sab_pom = Event.objects.filter(**sab_pom, kind="INCONTRI").exclude(
                registration_limit_from_same_scout_group__gte=0
            )

            assert (
                incontri_ven_mat.count()
                + incontri_ven_pom.count()
                + incontri_sab_mat.count()
                + incontri_sab_pom.count()
                == Event.objects.filter(kind="INCONTRI")
                .exclude(registration_limit_from_same_scout_group__gte=0)
                .count()
            )

            mapping = {
                rosso: [
                    None,
                    sguardi_ven_pom,
                    incontri_sab_mat,
                    confronti_sab_pom,
                ],
                viola: [
                    sguardi_ven_mat,
                    None,
                    confronti_sab_mat,
                    incontri_sab_pom,
                ],
                verde: [
                    incontri_ven_mat,
                    confronti_ven_pom,
                    None,
                    sguardi_sab_pom,
                ],
                giallo: [
                    confronti_ven_mat,
                    incontri_ven_pom,
                    sguardi_sab_mat,
                    None,
                ],
            }

            for district, events in mapping.items():
                for event_group in events:
                    if event_group is not None:
                        for event in event_group:
                            event.visibility_to_districts.add(district)
                            event.save()
