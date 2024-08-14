import pandas as pd
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from maps.models.location import Location
from people.models.district import District
from people.models.line import Line
from people.models.scout_group import ScoutGroup
from people.models.subdistrict import Subdistrict

User = get_user_model()


class Command(BaseCommand):
    help = "assegna file, sottcampi, contrade"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str, help="percorso del file da importare")

    def handle(self, *args, **options):
        with transaction.atomic():

            verde = District.objects.get_or_create(name="VERDE")[0]
            viola = District.objects.get_or_create(name="VIOLA")[0]
            rosso = District.objects.get_or_create(name="ROSSO")[0]
            giallo = District.objects.get_or_create(name="GIALLO")[0]
            district_mapping = {
                "1": verde,
                "2": viola,
                "3": rosso,
                "4": giallo,
            }

            path = options["path"]
            data_dict = pd.read_excel(path, sheet_name=None, dtype=str, na_filter=False)
            print("Importing CONTRADE")
            data = data_dict["CONTRADE"]
            for i, row in tqdm(data.iterrows(), total=len(data)):
                Subdistrict.objects.get_or_create(
                    name=row["NOME"], district=district_mapping[row["SOTTOCAMPO"]]
                )

            print("Importing FILE")
            data = data_dict["FILE"]
            for i, row in tqdm(data.iterrows(), total=len(data)):
                lat, lon = (x.strip() for x in row["COORDINATE"].split(","))
                location = Location.objects.get_or_create(
                    name=row["NOME"], defaults=dict(coords=Point(float(lon), float(lat)))
                )[0]
                subdistrict = Subdistrict.objects.get(name=row["CONTRADA"])
                Line.objects.get_or_create(
                    name=row["NOME"], subdistrict=subdistrict, location=location
                )

            print("assegnazione FILE")
            data = data_dict["GRUPPI"]
            for i, row in tqdm(data.iterrows(), total=len(data)):
                try:
                    scout_group = ScoutGroup.objects.get(name=row["Gruppo"])
                    line = Line.objects.get(name=row["FILA"])
                    scout_group.line = line
                    scout_group.save()
                except ScoutGroup.DoesNotExist:
                    print(f"failed scout group '{row['Gruppo']}' because it does not exist")
