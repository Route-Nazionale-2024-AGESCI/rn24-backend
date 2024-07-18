from unittest.mock import patch

import pytest
from django.conf import settings
from django.urls import reverse

from people.factories import SquadFactory


@pytest.mark.django_db
@patch("people.models.person.Person.qr_string_with_signature", return_value="AAAA")
def test_get_profile(mock, logged_api_client, person, base_squads_page):
    squad = SquadFactory()
    person.squads.add(squad)
    url = reverse("profile-detail")
    response = logged_api_client.get(url)
    assert response.status_code == 200
    assert response.json() == {
        "uuid": str(person.uuid),
        "agesci_id": str(person.agesci_id),
        "first_name": person.first_name,
        "last_name": person.last_name,
        "email": person.email,
        "phone": person.phone,
        "scout_group": {
            "uuid": str(person.scout_group.uuid),
            "name": person.scout_group.name,
            "zone": person.scout_group.zone,
            "region": person.scout_group.region,
            "line": {
                "uuid": str(person.scout_group.line.uuid),
                "name": person.scout_group.line.name,
                "location": str(person.scout_group.line.location.uuid),
                "subdistrict": {
                    "uuid": str(person.scout_group.line.subdistrict.uuid),
                    "name": person.scout_group.line.subdistrict.name,
                    "location": str(person.scout_group.line.subdistrict.location.uuid),
                    "district": {
                        "uuid": str(person.scout_group.line.subdistrict.district.uuid),
                        "name": person.scout_group.line.subdistrict.district.name,
                    },
                },
            },
            "happiness_path": person.scout_group.happiness_path,
        },
        "squads": [
            {
                "uuid": str(squad.uuid),
                "name": squad.name,
                "page": str(squad.page.uuid),
            },
        ],
        "public_key": settings.PUBLIC_KEY,
        "qr_code": "AAAA",
        "permissions": {
            "is_staff": False,
            "can_scan_qr": False,
        },
        "personal_data": {
            "identity_document_type": person.identity_document_type,
            "identity_document_number": person.identity_document_number,
            "identity_document_issue_date": person.identity_document_issue_date,
            "identity_document_expiry_date": person.identity_document_expiry_date,
            "accessibility_has_wheelchair": person.accessibility_has_wheelchair,
            "accessibility_has_caretaker_not_registered": person.accessibility_has_caretaker_not_registered,
            "sleeping_is_sleeping_in_tent": person.sleeping_is_sleeping_in_tent,
            "sleeping_requests": person.sleeping_requests,
            "sleeping_place": person.sleeping_place,
            "sleeping_requests_2": person.sleeping_requests_2,
            "food_diet_needed": person.food_diet_needed,
            "food_allergies": person.food_allergies,
            "food_is_vegan": person.food_is_vegan,
            "transportation_has_problems_moving_on_foot": person.transportation_has_problems_moving_on_foot,
            "transportation_need_transport": person.transportation_need_transport,
            "health_has_allergies": person.health_has_allergies,
            "health_allergies": person.health_allergies,
            "health_has_movement_disorders": person.health_has_movement_disorders,
            "health_movement_disorders": person.health_movement_disorders,
            "health_has_patologies": person.health_has_patologies,
            "health_patologies": person.health_patologies,
        },
    }
