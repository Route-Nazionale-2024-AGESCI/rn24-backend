from unittest.mock import patch

import pytest
from django.conf import settings
from django.urls import reverse


@pytest.mark.django_db
@patch("people.models.person.Person.qr_string_with_signature", return_value="AAAA")
def test_get_profile(mock, logged_api_client, person):
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
            "subdistrict": {
                "uuid": str(person.scout_group.subdistrict.uuid),
                "name": person.scout_group.subdistrict.name,
                "location": str(person.scout_group.subdistrict.location.uuid),
                "district": {
                    "uuid": str(person.scout_group.subdistrict.district.uuid),
                    "name": person.scout_group.subdistrict.district.name,
                },
            },
            "happiness_path": person.scout_group.happiness_path,
        },
        "squads": [],
        "public_key": settings.PUBLIC_KEY,
        "qr_code": "AAAA",
        "permissions": {
            "is_staff": False,
            "can_scan_qr": False,
        },
    }
