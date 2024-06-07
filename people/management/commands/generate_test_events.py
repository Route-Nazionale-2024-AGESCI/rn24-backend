from django.core.management.base import BaseCommand
from django.db import transaction

from events.factories import EventFactory
from people.models.district import District
from people.models.scout_group import ScoutGroup
from people.models.subdistrict import Subdistrict


class Command(BaseCommand):
    help = "generate some test Events"

    def split(self, a, n):
        k, m = divmod(len(a), n)
        return (a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n))

    @transaction.atomic
    def handle(self, *args, **options):

        # prima le mezze giornate
        # venerdì mattina 9-12
        # venerdì poermiggio 15-18
        # sabato mattina 9-12
        # sabato pomeriggio 15-18

        half_day_hours = (
            ("2024-08-23 09:00", "2024-08-23 12:00"),
            ("2024-08-23 15:00", "2024-08-23 18:00"),
            ("2024-08-24 09:00", "2024-08-24 12:00"),
            ("2024-08-24 15:00", "2024-08-24 18:00"),
        )

        district_1, district_2, district_3, district_4 = list(District.objects.all())

        # SGUARDI: 8+8+8+8
        # iscrizione personale, visibilità ad un sottocampo alla volta
        # CONFRONTI: 8+8+8+8
        # iscrizione personale, visibilità ad un sottocampo alla volta
        # INCONTRI: 100 + 100 + 100 + 100
        # iscrizione personale, visibilità ad un sottocampo alla volta
        # TRACCE: 100 + 100 + 100 + 100
        # iscrizione di gruppo (da backoffice), ma comunque sempre divisi per sottocampi

        SGUARDI_sequence = [district_1, district_2, district_3, district_4]
        CONFRONTI_sequence = [district_3, district_3, district_4, district_1]
        INCONTRI_sequence = [district_3, district_4, district_1, district_2]
        TRACCE_sequence = [district_4, district_1, district_2, district_3]

        print("SGUARDI")
        for i, (starts_at, ends_at) in enumerate(half_day_hours):
            district = SGUARDI_sequence[i]
            for i in range(1, 8 + 1):
                event = EventFactory(
                    name=f"Sguardi: evento di test numero {i}",
                    is_registration_required=True,
                    starts_at=starts_at,
                    ends_at=ends_at,
                    registration_limit=625,
                    kind="SGUARDI",
                )
                event.visibility_to_districts.add(district)

        print("CONFRONTI")
        for i, (starts_at, ends_at) in enumerate(half_day_hours):
            district = CONFRONTI_sequence[i]
            for i in range(1, 8 + 1):
                event = EventFactory(
                    name=f"Confronti: evento di test numero {i}",
                    is_registration_required=True,
                    starts_at=starts_at,
                    ends_at=ends_at,
                    registration_limit=625,
                    kind="CONFRONTI",
                )
                event.visibility_to_districts.add(district)

        print("INCONTRI")
        for i, (starts_at, ends_at) in enumerate(half_day_hours):
            district = INCONTRI_sequence[i]
            event_alfieri = EventFactory(
                name="Incontri: evento di test per gli alfieri",
                is_registration_required=True,
                starts_at=starts_at,
                ends_at=ends_at,
                registration_limit=625,
                registration_limit_from_same_scout_group=2,
                kind="INCONTRI",
            )
            event_alfieri.visibility_to_districts.add(district)
            for i in range(1, 100 + 1):
                event = EventFactory(
                    name=f"Incontri: evento di test numero {i}",
                    is_registration_required=True,
                    starts_at=starts_at,
                    ends_at=ends_at,
                    registration_limit=625,
                    kind="INCONTRI",
                )
                event.visibility_to_districts.add(district)

        print("TRACCE")
        for i, (starts_at, ends_at) in enumerate(half_day_hours):
            district = TRACCE_sequence[i]
            scout_groups = ScoutGroup.objects.filter(line__subdistrict__district=district).only(
                "id"
            )
            chunks = self.split(list(scout_groups), 100)
            for i in range(1, 100 + 1):
                event = EventFactory(
                    name=f"Tracce: evento di test numero {i}",
                    is_registration_required=False,
                    starts_at=starts_at,
                    ends_at=ends_at,
                    kind="TRACCE",
                )
                scout_groups = next(chunks)
                for scout_group in scout_groups:
                    event.registered_scout_groups.add(scout_group)

        # PASTI
        # per ora ipotizziamo siano per contrada
        print("PASTI")
        meal_times = (
            ("2024-08-22 20:00", "2024-08-22 20:30", "Cena"),  # cena giovedi
            ("2024-08-23 07:30", "2024-08-23 08:00", "Colazione"),  # colazione venerdi
            ("2024-08-23 12:30", "2024-08-23 13:00", "Pranzo"),  # pranzo venerdi
            ("2024-08-23 20:00", "2024-08-23 20:30", "Cena"),  # cena venerdì
            ("2024-08-24 07:30", "2024-08-24 08:00", "Colazione"),  # colazione sabato
            ("2024-08-24 12:30", "2024-08-24 13:00", "Pranzo"),  # pranzo sabato
            ("2024-08-24 20:00", "2024-08-24 20:30", "Cena"),  # cena sabato
            ("2024-08-25 07:30", "2024-08-25 08:00", "Colazione"),  # colazione domenica
            ("2024-08-25 12:30", "2024-08-25 13:00", "Pranzo"),  # pranzo domenica
        )
        for subdistrict in Subdistrict.objects.all():
            for starts_at, ends_at, name in meal_times:
                event = EventFactory(
                    name=name,
                    is_registration_required=False,
                    starts_at=starts_at,
                    ends_at=ends_at,
                    kind="PASTI",
                )
                event.registered_subdistricts.add(subdistrict)

        print("VENERDI sera: CONCERTO di sottocampo")
        for district in District.objects.all():
            event = EventFactory(
                name="Concerto di sottocampo",
                is_registration_required=False,
                starts_at="2024-08-23 21:00",
                ends_at="2024-08-23 22:30",
                kind="ALTRO",
            )
            event.registered_districts.add(district)

        print("SABATO mattina presto: doccia di contrada")
        for subdistrict in Subdistrict.objects.all():
            event = EventFactory(
                name="Doccia di contrada",
                is_registration_required=False,
                starts_at="2024-08-24 07:00",
                ends_at="2024-08-24 08:00",
                kind="DOCCIA",
            )
            event.registered_subdistricts.add(subdistrict)

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
