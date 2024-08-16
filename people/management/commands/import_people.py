from uuid import uuid4

import pandas as pd
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from people.models.person import Person
from people.models.squad import Squad

User = get_user_model()


class Command(BaseCommand):
    help = "importa persone da EXCEL"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str, help="percorso del file da importare")

    def handle(self, *args, **options):
        with transaction.atomic():
            path = options["path"]
            data_dict = pd.read_excel(path, sheet_name=None, dtype=str, na_filter=False)
            print("Importing PERSONE")
            data = data_dict["Foglio1"]
            for i, row in tqdm(data.iterrows(), total=len(data)):
                first_name = row["NOME (obbligatorio)"].strip().upper()
                last_name = row["COGNOME (obbligatorio)"].strip().upper()
                email = row["EMAIL (obbligatorio)"].strip()
                squad_name = row["RUOLO (obbligatorio)"].strip().upper()
                squad, _ = Squad.objects.get_or_create(name=squad_name)
                if not email:
                    email = f"{uuid4()}@example.com"
                person = Person.objects.filter(email=email).first()
                if not person:
                    person = Person.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                    )
                    person.user = User.objects.create_user(
                        username=email,
                        email=email,
                        first_name=first_name.strip(),
                        last_name=last_name.strip(),
                    )
                    person.save()
                person.squads.add(squad)
