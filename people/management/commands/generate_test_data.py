from django.core.management.base import BaseCommand
from django.db import IntegrityError
from tqdm import tqdm

from people.factories import (
    DistrictFactory,
    LineFactory,
    PersonFactory,
    ScoutGroupFactory,
    SquadFactory,
    SubdistrictFactory,
)

# some real numbers:
# 1600 scout groups
# 4 subdistrict (+ 1 special)
# 10 subdistricts per district
# 5 lines per subdistrict
# 8 scout groups per line
# 20_000 persons
# 13 person per scout_group


class Command(BaseCommand):
    help = "generate some test data to use for development and testing"

    def generate_item(self, factory, *args, **kwargs):
        try:
            item = factory(*args, **kwargs)
            return item
        except IntegrityError:
            # print(e)
            return self.generate_item(factory, *args, **kwargs)

    def handle(self, *args, **options):

        13 * 8 * 5 * 10 * 4
        district_names = ["ROSSO", "GIALLO", "VERDE", "VIOLA"]
        district_count = len(district_names)
        subdistricts = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "L"]
        subdistrict_count = len(subdistricts)
        line_count = 5
        scout_group_count = 8
        person_count = 13

        total_person_count = (
            district_count * subdistrict_count * line_count * scout_group_count * person_count
        )

        print(f"generating {total_person_count} persons")

        with tqdm(total=total_person_count) as pbar:
            for i in district_names:
                district = DistrictFactory(name=str(i))
                # print(district)
                for i in subdistricts:
                    subdistrict = SubdistrictFactory(
                        name=str(i),
                        district=district,
                    )
                    # print(subdistrict)
                    for i in range(1, line_count + 1):
                        line = LineFactory(
                            name=str(i),
                            subdistrict=subdistrict,
                        )
                        # print(line)
                        for i in range(1, scout_group_count + 1):
                            scout_group = self.generate_item(factory=ScoutGroupFactory, line=line)
                            # print(scout_group)

                            for i in range(1, person_count + 1):
                                person = self.generate_item(
                                    factory=PersonFactory, scout_group=scout_group
                                )
                                pbar.update(1)
                                # print(person)

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
                person = self.generate_item(factory=PersonFactory, scout_group=None)
                person.squads.add(squad)
                # print(person)
