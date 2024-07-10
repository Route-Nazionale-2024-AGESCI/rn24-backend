from datetime import datetime

import pandas as pd
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from events.models.event import Event
from maps.models.location import Location

User = get_user_model()


class Command(BaseCommand):
    help = "importa dati da un excel eventi"

    def add_arguments(self, parser):
        parser.add_argument("path", type=str, help="percorso del file da importare")

    def parse_boolean(self, value):
        if value.upper() in ["FALSE", "FALSO", "NO", "-", ""]:
            return False
        if value.upper() in ["TRUE", "VERO", "SI"]:
            return True
        raise ValueError(f"Invalid value '{value}'")

    def parse_datetime(self, date_string):
        # 23/8/24 09.00
        return datetime.strptime(date_string, "%d/%m/%y %H.%M")

    def handle(self, *args, **options):
        with transaction.atomic():
            path = options["path"]
            data_dict = pd.read_excel(path, sheet_name=None, dtype=str, na_filter=False)
            print("Importing LUOGHI")
            data = data_dict["LUOGHI"]
            for i, row in tqdm(data.iterrows(), total=len(data)):
                lat, lon = row["COORDINATE"].split(", ")
                Location.objects.get_or_create(
                    name=row["NOME"], defaults=dict(coords=Point(float(lon), float(lat)))
                )
            print("Importing EVENTI")
            data = data_dict["EVENTI"]
            for i, row in tqdm(data.iterrows(), total=len(data)):
                location = Location.objects.get(name=row["LUOGO"])
                name = row["TITOLO"]
                is_registration_required = row["è richiesta iscrizione personale?"]
                registration_limit = row["limite di iscritti"]
                registration_limit_from_same_scout_group = row["limite stesso gruppo"]
                starts_at = row["data inizio"]
                ends_at = row["data fine"]
                correlation_id = row["Correlation_ID"]
                registrations_open_at = row["data apertura iscrizioni"]
                registrations_close_at = row["data chiusura iscrizioni"]
                kind = row["tipologia"]
                event = Event.objects.create(
                    name=name,
                    location=location,
                    is_registration_required=self.parse_boolean(is_registration_required),
                    registration_limit=(int(registration_limit) if registration_limit else None),
                    registration_limit_from_same_scout_group=(
                        int(registration_limit_from_same_scout_group)
                        if registration_limit_from_same_scout_group
                        else None
                    ),
                    starts_at=self.parse_datetime(starts_at),
                    ends_at=self.parse_datetime(ends_at),
                    correlation_id=correlation_id,
                    registrations_open_at=(
                        self.parse_datetime(registrations_open_at)
                        if registrations_open_at
                        else None
                    ),
                    registrations_close_at=(
                        self.parse_datetime(registrations_close_at)
                        if registrations_close_at
                        else None
                    ),
                    kind=kind,
                )
                event.page.body = row["DESCRIZIONE"]
                event.page.save()
