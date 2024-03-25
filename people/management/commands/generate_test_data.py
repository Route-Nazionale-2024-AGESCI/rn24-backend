import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker

from authentication.models.user import User
from people.models.person import Person
from people.models.scout_group import HAPPINESS_PATH_CHOICES, ITALIAN_REGION_CHOICES, ScoutGroup
from people.models.squad import Squad
from people.models.subdistrict import Subdistrict


class Command(BaseCommand):
    help = "generate some test data to use for development and testing"

    def add_arguments(self, parser):
        # parser.add_argument("sample", nargs="+")
        pass

    def generate_person(self, fake, scout_group):
        return Person(
            agesci_id=random.randint(100000, 999999),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            codice_fiscale=fake.ssn(),
            birth_date=fake.date_of_birth(minimum_age=20, maximum_age=100),
            address=fake.address(),
            city=fake.city().upper(),
            scout_group=scout_group,
        )

    def handle(self, *args, **options):
        fake = Faker("it_IT")

        squads = [
            Squad.objects.create(name="Antincendio", description="Squadra antincendio"),
            Squad.objects.create(name="Pulizia bagni", description="La pattuglia più importante"),
            Squad.objects.create(name="Cucina", description="Minestron quanto è buon"),
            Squad.objects.create(name="Controllo accessi", description="Controllano gli accessi"),
            Squad.objects.create(name="Tangram Team", description="I volontari del tangram"),
            Squad.objects.create(name="Staff", description="Gli organizzatori della route"),
            Squad.objects.create(name="Ospiti", description="Forse non sono scout"),
        ]
        for squad in squads:
            for i in range(10):
                person = self.generate_person(fake, None)
                person.save()
                person.squads.add(squad)

        for i in range(100):

            scout_group = ScoutGroup(
                name=fake.city().upper() + " " + str(random.randint(1, 256)),
                zone=fake.administrative_unit().upper(),
                region=random.choice(ITALIAN_REGION_CHOICES)[0],
                subdistrict=Subdistrict.objects.order_by("?").first(),
                happiness_path=random.choice(HAPPINESS_PATH_CHOICES)[0],
                arrived_at=None,
            )
            scout_group.save()
            print(scout_group.__dict__)

            for i in range(20):
                person = self.generate_person(fake, scout_group)
                try:
                    person.save()
                except IntegrityError as e:
                    if "duplicate key value violates unique constraint" in str(e):
                        continue
                    raise
                print(person.__dict__)

                user = User(
                    username=person.agesci_id,
                    email=person.email,
                    first_name=person.first_name,
                    last_name=person.last_name,
                )
                user.save()
                person.user = user
                person.save()
