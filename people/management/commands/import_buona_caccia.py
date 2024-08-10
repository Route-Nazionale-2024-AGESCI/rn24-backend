import csv
from datetime import datetime
from io import StringIO

import pandas as pd
import requests
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

    mapping = {
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
            except Exception:
                return None

    def clean_food_diet(self, diet):
        if diet == "Monodieta (selezionare nel caso di singola allergia/intolleranza)":
            return "Monodieta"
        if diet.startswith(
            "Dieta da shock (selezionare nel caso di una o più allergie che possano causare shock anafilattico)"
        ):
            return "Dieta da shock"
        if diet == "Multidieta (selezionare nel caso di più allergie/intolleranze)":
            return "Multidieta"
        return diet

    def parse_food_allergies(self, col1, col2):
        if col2:
            return col1 + " - " + col2
        return col1

    def parse_boolean(self, value):
        if value.upper() in ["NO", "-", ".", ""]:
            return False
        if value.upper() in [
            "SI",
            "SI, SONO INCINTA NECESSITO DI NAVETTA",
            "NON POSSO FARE STRADA CON LO ZAINO",
            "DISABILE CHE DEAMBULA, MA MALE E LENTAMENTE",
        ]:
            return True
        elif "SI" in value.upper():
            return True
        raise ValueError(f"Invalid value '{value}'")

    def get_value(self, row, key, default=""):
        for col in self.mapping[key]:
            if col in row:
                return row[col].strip()
        return default

    def fetch_scout_group_happines_old_old(self):
        url = "https://rn24.agesci.it/wp-json/rn24/v1/boxes/export"
        response = requests.get(url, verify=False)
        response.raise_for_status()
        csv_content = response.content.decode("utf-8-sig")
        data = {}
        happiness_path_set = set()
        csv_reader = csv.DictReader(StringIO(csv_content), delimiter=";")
        for row in csv_reader:
            d = {}
            d["name"] = row["Gruppo"].strip().upper()
            d["agesci_id"] = row["Codice gruppo"]
            d["happiness"] = row["Felici di..."]
            happiness_path_set.add(d["happiness"])
            data[d["name"]] = d
        print(list(happiness_path_set))
        return data

    def fetch_scout_group_happines_old(self):
        data_dict = pd.read_excel(
            "imports/felici.xlsx", sheet_name=None, dtype=str, na_filter=False
        )["Sheet1"]
        happy_mapping = {
            "accogliere": "Felici di accogliere",
            "vivere una vita giusta": "Felici di vivere una vita giusta",
            "prendersi cura e custodire": "Felici di prendersi cura e custodire",
            "generare speranza": "Felici di generare speranza",
            "fare esperienza di Dio": "Felici di fare esperienza di Dio",
            "essere appassiona-ti": "Felici di essere appassionati",
            "lavorare per la pace": "Felici di lavorare per la pace",
            "essere profeti di un nuovo mondo": "Felici di essere profeti in un mondo nuovo",
        }
        data = {}
        happiness_path_set = set()
        for i, row in data_dict.iterrows():
            d = {}
            d["name"] = row["GRUPPO"].strip().upper()
            d["happiness"] = happy_mapping[row["FELICI DI"]]
            d["agesci_id"] = None
            data[d["name"]] = d
            happiness_path_set.add(d["happiness"])
        print(list(happiness_path_set))
        return data

    def fetch_scout_group_happines(self):
        data_dict = pd.read_excel(
            "imports/Sottocampi_def_6ago.xls", sheet_name=None, dtype=str, na_filter=False
        )["Sheet1"]
        data = {}
        happiness_path_set = set()
        for i, row in data_dict.iterrows():
            d = {}
            d["name"] = row["Gruppo"].strip().upper()
            d["happiness"] = row["Felici_def"]
            d["agesci_id"] = None
            d["district"] = row["SOTTOCAMPO"]
            data[d["name"]] = d
            happiness_path_set.add(d["happiness"])
        print(list(happiness_path_set))
        return data

    def map_food_diet(self):
        data_dict = pd.read_excel(
            "imports/Agesci_estrazione_utente_dieta.xlsx",
            sheet_name=None,
            dtype=str,
            na_filter=False,
        )["Sheet1"]
        data = {}
        for i, row in data_dict.iterrows():
            data[row["MATRICOLA"]] = row["DIETA "]
        return data

    def handle(self, *args, **options):
        self.scout_group_happiness = self.fetch_scout_group_happines()
        self.food_diet = self.map_food_diet()
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
                "Kingereheim 12-15",
                "Kinderheim 4-11",
                "Kinderheim",
                'Persone "esterne" da considerar',
            ]
            if list(data_dict.keys()) != sheet_names:
                self.stdout.write(self.style.ERROR("Sheets not matching, something changed!"))
                print(list(data_dict.keys()))
                print(sheet_names)
                return
            # for sheet_name in sheet_names:
            #     if sheet_name in [
            #         "ritirati",
            #         "Kinderheim",
            #         'Persone "esterne" da considerar',
            #         "Tangram Team",
            #         "iscrizioni ",  # DON'T COMMIT ME
            #     ]:
            #         continue
            #     self.import_sheet(sheet_name, data_dict)
            # e ora il tangram team!
            data_dict = pd.read_excel(
                "imports/FILE TANGRAM OPERATIVO.xlsx",
                sheet_name="Tangram Team",
                dtype=str,
                na_filter=False,
            )
            self.import_sheet("Tangram Team", data_dict)

    def import_sheet(self, sheet_name, data_dict):
        print(f"Importing {sheet_name}")
        squad, _ = Squad.objects.get_or_create(name=sheet_name.strip().upper())
        if sheet_name == "Tangram Team":
            data = data_dict
        else:
            data = data_dict[sheet_name]
        for i, row in tqdm(data.iterrows(), total=len(data)):
            if sheet_name in [
                "iscrizioni ",
                "Kindereheim 0-3",
                "Kinderheim 4-11",
                "Kingereheim 12-15",
            ]:
                scout_group_name = self.get_value(row, "group_name").strip().upper()
                if scout_group_name not in self.scout_group_happiness:
                    print(f"group not found in happiness file: '{scout_group_name}'")
                    happiness_path = None
                    group_agesci_id = None
                else:
                    happiness_path = self.scout_group_happiness[scout_group_name]["happiness"]
                    group_agesci_id = self.scout_group_happiness[scout_group_name]["agesci_id"]
                scout_group, _ = ScoutGroup.objects.get_or_create(
                    name=scout_group_name,
                    defaults=dict(
                        zone=self.get_value(row, "group_zone").strip().upper(),
                        region=self.get_value(row, "group_region").strip().upper(),
                        agesci_id=group_agesci_id,
                        happiness_path=happiness_path,
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
                        print(f"{existing_person} is in Tangram Team but was already registered")
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
            if agesci_id in self.food_diet:
                food_allergies = self.food_diet[agesci_id]
            else:
                food_allergies = None
            if agesci_id == "vescovo":
                continue
            if agesci_id == "":
                agesci_id = None
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
                food_diet_needed=self.clean_food_diet(self.get_value(row, "food_diet_needed")),
                # food_allergies=self.parse_food_allergies(
                #     self.get_value(row, "food_allergies_1"),
                #     self.get_value(row, "food_allergies_2"),
                # ),
                food_allergies=food_allergies,
                food_is_vegan=self.parse_boolean(self.get_value(row, "food_is_vegan")),
                transportation_has_problems_moving_on_foot=self.parse_boolean(
                    self.get_value(row, "transportation_has_problems_moving_on_foot")
                ),
                transportation_need_transport=self.get_value(row, "transportation_need_transport"),
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
            if sheet_name == "Tangram Team":
                tangram_squad_names = [
                    x.strip() for x in row["TEAM DI SERVIZIO PER APP"].split(",") if x.strip()
                ]
                if tangram_squad_names:
                    for tangram_squad_name in tangram_squad_names:
                        # print(f"squad name: '{tangram_squad_name}'")
                        tangram_squad, _ = Squad.objects.get_or_create(
                            name="T-" + tangram_squad_name
                        )
                        person.squads.add(tangram_squad)
