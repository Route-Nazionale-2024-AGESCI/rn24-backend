import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from tqdm import tqdm

from people.models.person import Person
from people.models.scout_group import ScoutGroup


class Command(BaseCommand):
    help = "importa dati da BuonaCaccia"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str, help="percorso del file da importare")

    def handle(self, *args, **options):
        path = options["path"]
        with open(path) as file:
            reader = csv.DictReader(file, delimiter=";")
            for row in tqdm(reader):
                try:
                    scout_group, _ = ScoutGroup.objects.get_or_create(
                        name=row["Gruppo"],
                        defaults=dict(
                            zone=row["Zona"],
                            region=row["Regione"].upper(),
                        ),
                    )
                    person, _ = Person.objects.get_or_create(
                        agesci_id=row["Codice"],
                        defaults=dict(
                            first_name=row["Nome"],
                            last_name=row["Cognome"],
                            birth_date=datetime.strptime(row["DataNascita"], "%d/%m/%Y"),
                            gender=row["Sesso"],
                            training_level=row["FoCa"],
                            address=row["Indirizzo"],
                            zip_code=row["CAP"],
                            city=row["Città"],
                            province=row["PR"],
                            region=row["Regione"].upper(),
                            email=row["EmailContatto"],
                            phone=row["CellContatto"],
                            scout_group=scout_group,
                        ),
                    )
                except Exception as e:
                    print(e)
