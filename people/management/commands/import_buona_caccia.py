from datetime import datetime

import pandas as pd
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from people.models.person import Person
from people.models.scout_group import ScoutGroup

User = get_user_model()


class Command(BaseCommand):
    help = "importa dati da BuonaCaccia"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str, help="percorso del file da importare")

    def parse_birth_date(self, date_string):
        try:
            return datetime.strptime(date_string.split(" ")[0], "%Y-%m-%d")
        except Exception as e:
            print(e)
            return None

    def parse_food_allergies(self, col1, col2):
        if col2:
            return col1 + " - " + col2
        return col1

    def parse_boolean(self, value):
        if value.upper() in ["NO", "-"]:
            return False
        if value.upper() in ["SI"]:
            return True
        raise ValueError(f"Invalid value '{value}'")

    def handle(self, *args, **options):
        with transaction.atomic():
            path = options["path"]
            data_dict = pd.read_excel(path, sheet_name=None, dtype=str, na_filter=False)
            sheet_names = [
                "iscrizioni ",
                "tardive plus senza viaggio",
                "Tangram Team",
                "Tangram Team Staff",
                "Comitato",
                "delegazioni straniere",
                "Kindereheim 0-3",
                "Kinderheim 4-11",
                "Kingereheim 12-15",
                "Kinderheim",
            ]
            if list(data_dict.keys()) != sheet_names:
                self.stdout.write(self.style.ERROR("Sheets not matching, something changed!"))
                return
            # iscrizioni
            data = data_dict["iscrizioni "]
            for i, row in tqdm(data.iterrows()):
                scout_group, _ = ScoutGroup.objects.get_or_create(
                    name=row["Gruppo"].strip().upper(),
                    defaults=dict(
                        zone=row["Zona"].strip().upper(),
                        region=row["Regione"].strip().upper(),
                    ),
                )
                user = User.objects.create(
                    username=row["Codice"],
                    email=row["EmailContatto"].strip(),
                    first_name=row["Nome"].strip().upper(),
                    last_name=row["Cognome"].strip().upper(),
                )
                Person.objects.create(
                    agesci_id=row["Codice"].strip(),
                    user=user,
                    first_name=row["Nome"].strip().upper(),
                    last_name=row["Cognome"].strip().upper(),
                    birth_date=self.parse_birth_date(row["DataNascita"]),
                    gender=row["Sesso"].strip(),
                    training_level=row["FoCa"].strip(),
                    address=row["Indirizzo"].strip(),
                    zip_code=row["CAP"].strip(),
                    city=row["Città"].strip(),
                    province=row["PR"].strip(),
                    region=row["Regione"].strip().upper(),
                    email=row["EmailContatto"].strip(),
                    phone=str(row["CellContatto"]),
                    scout_group=scout_group,
                    accessibility_has_wheelchair=self.parse_boolean(
                        row["Sei un/a capo/a con sedia a rotelle?"]
                    ),
                    accessibility_has_caretaker_not_registered=self.parse_boolean(
                        row[
                            "Sei un/a capo/a che per motivi di disabilità/patologie/età viaggia con accompagnatore NON iscritto alla RN24?"
                        ]
                    ),
                    sleeping_is_sleeping_in_tent=self.parse_boolean(
                        row["Dormo in tenda personale."]
                    ),
                    sleeping_requests=row[
                        "Inserisci qui eventuali richieste legate a disabilità/patologie in merito al pernotto in tenda personale."
                    ],
                    sleeping_place=row["Per motivi di disabilità/patologie ho bisogno di dormire:"],
                    sleeping_requests_2=row[
                        "Inserisci qui eventuali richieste legate a disabilità/patologie in merito al pernotto in tenda personale..1"
                    ],
                    food_diet_needed=row["Allergie/intolleranze ad alimenti da segnalare."],
                    food_allergies=self.parse_food_allergies(
                        row["Selezionare una o più allergie/intolleranze elencate:"],
                        row["Se hai indicato altro specificalo qui:"],
                    ),
                    food_is_vegan=self.parse_boolean(row["Segui una dieta vegana?"]),
                    transportation_has_problems_moving_on_foot=self.parse_boolean(
                        row[
                            "Hai disabilità/patologie/età che non ti permettono di sostenere gli spostamenti a piedi previsti?"
                        ]
                    ),
                    transportation_need_transport=row[
                        "Necessiti di un accompagnatore fornito dall'organizzazione durante l'evento?"
                    ],
                    health_has_allergies=self.parse_boolean(row["Hai allergie accertate?"]),
                    health_allergies=row[
                        'Se hai risposto "si" alla precedene domanda specifica quali:'
                    ],
                    health_has_movement_disorders=self.parse_boolean(
                        row["Sei affetto da disturbi motori?"]
                    ),
                    health_movement_disorders=row[
                        'Se hai risposto "si" alla precedene domanda specifica quali:.1'
                    ],
                    health_has_patologies=self.parse_boolean(
                        row["Sei affetto da patologie cardiovascolari/respiratorie/neurologiche? "]
                    ),
                    health_patologies=row[
                        'Se hai risposto "si" alla precedene domanda specifica quali:.2'
                    ],
                )
