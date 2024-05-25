from django.core.management.base import BaseCommand
from django.db import transaction

from events.factories import EventFactory
from people.models.district import District
from people.models.scout_group import ScoutGroup
from people.models.subdistrict import Subdistrict


class Command(BaseCommand):
    help = "generate some test Events"

    @transaction.atomic
    def handle(self, *args, **options):
        print("GIOVEDI: arrivo e cena")
        for scout_group in ScoutGroup.objects.all().iterator():
            event = EventFactory(
                name="Cena",
                is_registration_required=False,
                starts_at="2024-08-22 19:00",
                ends_at="2024-08-22 21:00",
                kind="PASTI",
            )
            event.registered_scout_groups.add(scout_group)

        print("VENERDI mattina: SGUARDI")
        sguardi = []
        for i in range(6):
            sguardi.append(
                EventFactory(
                    name=f"Sguardi: evento di test numero {i}",
                    is_registration_required=True,
                    starts_at="2024-08-23 09:00",
                    ends_at="2024-08-23 12:00",
                    registration_limit=10,
                    kind="SGUARDI",
                )
            )
        for scout_group in ScoutGroup.objects.all().iterator():
            for event in sguardi:
                event.visibility_to_scout_groups.add(scout_group)

        print("VENERDI pranzo")
        for scout_group in ScoutGroup.objects.all().iterator():
            event = EventFactory(
                name="Pranzo",
                is_registration_required=False,
                starts_at="2024-08-23 12:00",
                ends_at="2024-08-23 14:00",
                kind="PASTI",
            )
            event.registered_scout_groups.add(scout_group)

        print("VENERDI pomeriggio: CONFRONTI")
        sguardi = []
        for i in range(6):
            sguardi.append(
                EventFactory(
                    name=f"Confronti: evento di test numero {i}",
                    is_registration_required=True,
                    starts_at="2024-08-23 15:00",
                    ends_at="2024-08-23 19:00",
                    registration_limit=10,
                    kind="CONFRONTI",
                )
            )
        for scout_group in ScoutGroup.objects.all().iterator():
            for event in sguardi:
                event.visibility_to_scout_groups.add(scout_group)

        print("VENERDI cena")
        for scout_group in ScoutGroup.objects.all().iterator():
            event = EventFactory(
                name="Cena",
                is_registration_required=False,
                starts_at="2024-08-23 19:30",
                ends_at="2024-08-23 20:30",
                kind="PASTI",
            )
            event.registered_scout_groups.add(scout_group)

        print("VENERDI sera: CONCERTO di sottocampo")
        for district in District.objects.all():
            event = EventFactory(
                name="Concerto di band strepitosa nel sottocampo",
                is_registration_required=False,
                starts_at="2024-08-23 21:30",
                ends_at="2024-08-23 23:00",
                kind="ALTRO",
            )
            event.registered_districts.add(district)

        print("SABATO mattina presto: doccia di contrada")
        for subdistrict in Subdistrict.objects.all().iterator():
            event = EventFactory(
                name="Doccia di contrada",
                is_registration_required=False,
                starts_at="2024-08-24 07:30",
                ends_at="2024-08-24 08:30",
                kind="DOCCIA",
            )
            event.registered_subdistricts.add(subdistrict)

        print("SABATO mattina: TRACCE")
        for scout_group in ScoutGroup.objects.all().iterator():
            event = EventFactory(
                name="Tracce: evento di test",
                is_registration_required=False,
                starts_at="2024-08-24 09:00",
                ends_at="2024-08-24 12:00",
                kind="TRACCE",
            )
            event.registered_scout_groups.add(scout_group)

        print("SABATO pranzo")
        for scout_group in ScoutGroup.objects.all().iterator():
            event = EventFactory(
                name="Pranzo",
                is_registration_required=False,
                starts_at="2024-08-24 12:30",
                ends_at="2024-08-24 14:00",
                kind="PASTI",
            )
            event.registered_scout_groups.add(scout_group)

        print("SABATO pomeriggio: INCONTRI (alfieri)")
        evento_alfieri = EventFactory(
            name="Incontri: (per alfieri)",
            is_registration_required=True,
            starts_at="2024-08-24 14:30",
            ends_at="2024-08-24 18:30",
            registration_limit_from_same_scout_group=2,
            kind="INCONTRI",
        )
        for scout_group in ScoutGroup.objects.all().iterator():
            evento_alfieri.visibility_to_scout_groups.add(scout_group)

        print("SABATO pomeriggio: INCONTRI")
        incontri = []
        for i in range(6):
            incontri.append(
                EventFactory(
                    name=f"Incontri: evento di test numero {i}",
                    is_registration_required=True,
                    starts_at="2024-08-24 15:00",
                    ends_at="2024-08-23 19:00",
                    registration_limit=10,
                    kind="INCONTRI",
                )
            )
        for scout_group in ScoutGroup.objects.all().iterator():
            for event in incontri:
                event.visibility_to_scout_groups.add(scout_group)

        print("SABATO cena")
        for scout_group in ScoutGroup.objects.all().iterator():
            event = EventFactory(
                name="Cena",
                is_registration_required=False,
                starts_at="2024-08-24 19:30",
                ends_at="2024-08-24 20:30",
                kind="PASTI",
            )
            event.registered_scout_groups.add(scout_group)

        for district in District.objects.all():
            event = EventFactory(
                name="È ora di partire per il concerto",
                is_registration_required=False,
                starts_at="2024-08-24 21:00",
                ends_at="2024-08-24 21:30",
                kind="LOGISTICO",
            )
            event.registered_districts.add(district)

        print("SABATO sera: CONCERTO per TUTTI")
        mega_concerto = EventFactory(
            name="MEGA CONCERTO per TUTTI",
            is_registration_required=False,
            starts_at="2024-08-24 21:30",
            ends_at="2024-08-24 23:00",
            kind="ALTRO",
        )
        for district in District.objects.all():
            mega_concerto.registered_districts.add(district)

        print("DOMENICA mattina: MESSA")
        mega_concerto = EventFactory(
            name="Messa",
            is_registration_required=False,
            starts_at="2024-08-25 10:00",
            ends_at="2024-08-25 12:00",
            kind="ALTRO",
        )
        for district in District.objects.all():
            mega_concerto.registered_districts.add(district)
