from datetime import datetime

import pandas as pd
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from people.models.person import Person
from people.models.scout_group import ScoutGroup
from people.models.squad import Squad

User = get_user_model()


class Command(BaseCommand):
    help = "importa dati da BuonaCaccia"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str, help="percorso del file da importare")

    def parse_date(self, date_string):
        if not date_string:
            return
        try:
            return datetime.strptime(date_string.split(" ")[0], "%Y-%m-%d")
        except Exception:
            try:
                return datetime.strptime(date_string.split(" ")[0], "%d.%m.%Y")
            except Exception as e:
                print(e)
                return None

    def parse_food_allergies(self, col1, col2):
        if col2:
            return col1 + " - " + col2
        return col1

    def parse_boolean(self, value):
        if value.upper() in ["NO", "-", ""]:
            return False
        if value.upper() in [
            "SI",
            "SI, SONO INCINTA NECESSITO DI NAVETTA",
            "NON POSSO FARE STRADA CON LO ZAINO",
        ]:
            return True
        raise ValueError(f"Invalid value '{value}'")

    def get_value(self, row, key, default=""):
        for col in self.mapping[key]:
            if col in row:
                return row[col].strip()
        return default

    def handle(self, *args, **options):
        with transaction.atomic():
            path = options["path"]
            data_dict = pd.read_excel(path, sheet_name=None, dtype=str, na_filter=False)
            sheet_names = [
                "iscrizioni ",
                "delegazioni straniere",
                "ritirati",
                "Tangram Team",
                "Tangram Team Staff",
                "Comitato",
                "Collaboratori",
                "Kindereheim 0-3",
                "Kinderheim 4-11",
                "Kingereheim 12-15",
            ]
            self.mapping = {
                "group_name": [
                    "Gruppo",
                ],
                "group_zone": [
                    "Zona",
                ],
                "group_region": [
                    "Regione",
                ],
                "agesci_id": [
                    "Codice",
                ],
                "email": [
                    "EmailContatto",
                    "Email personale",
                ],
                "first_name": [
                    "Nome",
                    "Nome2",
                ],
                "last_name": [
                    "Cognome",
                ],
                "birth_date": [
                    "DataNascita",
                ],
                "gender": [
                    "Sesso",
                ],
                "training_level": [
                    "FoCa",
                ],
                "address": [
                    "Indirizzo",
                ],
                "zip_code": [
                    "CAP",
                ],
                "city": [
                    "Città",
                ],
                "province": [
                    "PR",
                ],
                "region": [
                    "Regione",
                ],
                "phone": [
                    "CellContatto",
                    "Cell Personale",
                ],
                "identity_document_type": [
                    "Tipologia documento:",
                ],
                "identity_document_number": [
                    "Indica il numero del documento.",
                ],
                "identity_document_issue_date": [
                    "Data rilascio documento (GG/MM/AAAA)/",
                ],
                "identity_document_expiry_date": [
                    "Data scadenza (GG/MM/AAAA)/",
                ],
                "accessibility_has_wheelchair": [
                    "Sei un/a capo/a con sedia a rotelle?",
                ],
                "accessibility_has_caretaker_not_registered": [
                    "Sei un/a capo/a che per motivi di disabilità/patologie/età viaggia con accompagnatore NON iscritto alla RN24?",
                ],
                "sleeping_is_sleeping_in_tent": [
                    "Dormo in tenda personale.",
                    "Confermo di dormire in tenda personale",
                ],
                "sleeping_requests": [
                    "Inserisci qui eventuali richieste legate a disabilità/patologie in merito al pernotto in tenda personale.",
                ],
                "sleeping_place": [
                    "Per motivi di disabilità/patologie ho bisogno di dormire:",
                ],
                "sleeping_requests_2": [
                    "Inserisci qui eventuali richieste legate a disabilità/patologie in merito al pernotto in tenda personale..1",
                ],
                "food_diet_needed": [
                    "Allergie/intolleranze ad alimenti da segnalare.",
                    "Allergie/intolleranze ad alimenti da segnalare",
                ],
                "food_allergies_1": [
                    "Selezionare una o più allergie/intolleranze elencate:",
                    "Selezionare nelle allergie/intolleranze elencate",
                ],
                "food_allergies_2": [
                    "Se hai indicato altro specificalo qui:",
                    "Altro (inserire eventuali alimenti a cui sei allergico/intollerante non presenti nella lista)",
                ],
                "food_is_vegan": [
                    "Segui una dieta vegana?",
                ],
                "transportation_has_problems_moving_on_foot": [
                    "Hai disabilità/patologie/età che non ti permettono di sostenere gli spostamenti a piedi previsti?",
                ],
                "transportation_need_transport": [
                    "Necessiti di un accompagnatore fornito dall'organizzazione durante l'evento?",
                ],
                "health_has_allergies": [
                    "Hai allergie accertate?",
                    "Allergie accertate",
                ],
                "health_allergies": [
                    'Se hai risposto "si" alla precedene domanda specifica quali:',
                    'Se hai risposto "si" alla precedene domanda specifica',
                ],
                "health_has_movement_disorders": [
                    "Sei affetto da disturbi motori?",
                    "Disturbi motori",
                ],
                "health_movement_disorders": [
                    'Se hai risposto "si" alla precedene domanda specifica quali:.1',
                    'Se hai risposto "si" alla precedene domanda specifica2',
                ],
                "health_has_patologies": [
                    "Sei affetto da patologie cardiovascolari/respiratorie/neurologiche? ",
                    "Patologie Cardiovascolari - Respiratorie - Neurologiche ",
                ],
                "health_patologies": [
                    'Se hai risposto "si" alla precedene domanda specifica quali:.2',
                    'Se hai risposto "si" alla precedene domanda specifica3',
                ],
                "kid_first_name": ["Nome bambina/o"],
                "kid_last_name": ["Cognome bambina/o"],
                "kid_birth_date": ["Data di nascita (gg-mm-aaaa)"],
            }
            if list(data_dict.keys()) != sheet_names + [
                "Kinderheim",
            ]:
                self.stdout.write(self.style.ERROR("Sheets not matching, something changed!"))
                print(list(data_dict.keys()))
                print(sheet_names)
                return
            for sheet_name in sheet_names:
                if sheet_name in ["ritirati", "Collaboratori"]:
                    continue
                print(f"Importing {sheet_name}")
                squad, _ = Squad.objects.get_or_create(name=sheet_name.strip().upper())
                data = data_dict[sheet_name]
                for i, row in tqdm(data.iterrows(), total=len(data)):
                    if sheet_name in [
                        "iscrizioni ",
                    ]:
                        scout_group, _ = ScoutGroup.objects.get_or_create(
                            name=self.get_value(row, "group_name").strip().upper(),
                            defaults=dict(
                                zone=self.get_value(row, "group_zone").strip().upper(),
                                region=self.get_value(row, "group_region").strip().upper(),
                            ),
                        )
                    else:
                        scout_group = None
                    agesci_id = self.get_value(row, "agesci_id", None)
                    if agesci_id:
                        username = agesci_id
                    else:
                        username = self.get_value(row, "email")

                    if sheet_name in ["Kindereheim 0-3", "Kinderheim 4-11", "Kingereheim 12-15"]:
                        user = None
                        first_name = self.get_value(row, "kid_first_name").strip().upper()
                        last_name = self.get_value(row, "kid_last_name").strip().upper()
                        birth_date = self.get_value(row, "kid_birth_date").strip().upper()
                        notes = f"codice AGESCI genitore: {agesci_id}"
                        agesci_id = None
                    else:
                        if sheet_name == "Tangram Team":
                            existing_person = Person.objects.filter(agesci_id=agesci_id).first()
                            if existing_person:
                                existing_person.squads.add(squad)
                                print(
                                    f"{existing_person} is in Tangram Team but was already registered"
                                )
                                continue

                        first_name = self.get_value(row, "first_name").strip().upper()
                        last_name = self.get_value(row, "last_name").strip().upper()
                        birth_date = self.get_value(row, "birth_date").strip().upper()
                        notes = None
                        user = User.objects.create(
                            username=username,
                            email=self.get_value(row, "email").strip(),
                            first_name=first_name,
                            last_name=last_name,
                        )
                    person = Person.objects.create(
                        agesci_id=agesci_id,
                        user=user,
                        first_name=first_name,
                        last_name=last_name,
                        birth_date=self.parse_date(birth_date),
                        gender=self.get_value(row, "gender").strip(),
                        training_level=self.get_value(row, "training_level").strip(),
                        address=self.get_value(row, "address").strip(),
                        zip_code=self.get_value(row, "zip_code").strip(),
                        city=self.get_value(row, "city").strip(),
                        province=self.get_value(row, "province").strip(),
                        region=self.get_value(row, "region").strip().upper(),
                        email=self.get_value(row, "email").strip(),
                        phone=str(self.get_value(row, "phone")),
                        scout_group=scout_group,
                        identity_document_type=self.get_value(row, "identity_document_type"),
                        identity_document_number=self.get_value(row, "identity_document_number"),
                        identity_document_issue_date=self.parse_date(
                            self.get_value(row, "identity_document_issue_date")
                        ),
                        identity_document_expiry_date=self.parse_date(
                            self.get_value(row, "identity_document_expiry_date")
                        ),
                        accessibility_has_wheelchair=self.parse_boolean(
                            self.get_value(row, "accessibility_has_wheelchair")
                        ),
                        accessibility_has_caretaker_not_registered=self.parse_boolean(
                            self.get_value(row, "accessibility_has_caretaker_not_registered")
                        ),
                        sleeping_is_sleeping_in_tent=self.parse_boolean(
                            self.get_value(row, "sleeping_is_sleeping_in_tent")
                        ),
                        sleeping_requests=self.get_value(row, "sleeping_requests"),
                        sleeping_place=self.get_value(row, "sleeping_place"),
                        sleeping_requests_2=self.get_value(row, "sleeping_requests_2"),
                        food_diet_needed=self.get_value(row, "food_diet_needed"),
                        food_allergies=self.parse_food_allergies(
                            self.get_value(row, "food_allergies_1"),
                            self.get_value(row, "food_allergies_2"),
                        ),
                        food_is_vegan=self.parse_boolean(self.get_value(row, "food_is_vegan")),
                        transportation_has_problems_moving_on_foot=self.parse_boolean(
                            self.get_value(row, "transportation_has_problems_moving_on_foot")
                        ),
                        transportation_need_transport=self.get_value(
                            row, "transportation_need_transport"
                        ),
                        health_has_allergies=self.parse_boolean(
                            self.get_value(row, "health_has_allergies")
                        ),
                        health_allergies=self.get_value(row, "health_allergies"),
                        health_has_movement_disorders=self.parse_boolean(
                            self.get_value(row, "health_has_movement_disorders")
                        ),
                        health_movement_disorders=self.get_value(row, "health_movement_disorders"),
                        health_has_patologies=self.parse_boolean(
                            self.get_value(row, "health_has_patologies")
                        ),
                        health_patologies=self.get_value(row, "health_patologies"),
                        notes=notes,
                    )
                    if squad:
                        person.squads.add(squad)
