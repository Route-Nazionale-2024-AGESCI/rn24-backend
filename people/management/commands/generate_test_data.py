from django.core.management.base import BaseCommand
from django.db import IntegrityError

from people.factories import (
    PersonFactory,
    SquadFactory,
    DistrictFactory,
    SubdistrictFactory,
    ScoutGroupFactory,
)


class Command(BaseCommand):
    help = "generate some test data to use for development and testing"

    def generate_person(self, *args, **kwargs):
        try:
            person = PersonFactory(*args, **kwargs)
            return person
        except IntegrityError as e:
            print(e)
            return self.generate_person(*args, **kwargs)

    def handle(self, *args, **options):

        for i in range(1, 5):
            district = DistrictFactory(name=str(i))
            print(district)
            for i in range(5):
                subdistrict = SubdistrictFactory(district=district)
                print(subdistrict)
                for i in range(20):
                    scout_group = ScoutGroupFactory(subdistrict=subdistrict)
                    print(scout_group)

                    for i in range(20):
                        person = self.generate_person(scout_group=scout_group)
                        print(person)

        squads = [
            SquadFactory(name="Antincendio", description="Squadra antincendio"),
            SquadFactory(name="Pulizia bagni", description="La pattuglia più importante"),
            SquadFactory(name="Cucina", description="Minestron quanto è buon"),
            SquadFactory(name="Controllo accessi", description="Controllano gli accessi"),
            SquadFactory(name="Tangram Team", description="I volontari del tangram"),
            SquadFactory(name="Staff", description="Gli organizzatori della route"),
            SquadFactory(name="Ospiti", description="Forse non sono scout"),
        ]
        for squad in squads:
            print(squad)
            for i in range(10):
                person = self.generate_person(scout_group=None)
                person.squads.add(squad)
                print(person)
