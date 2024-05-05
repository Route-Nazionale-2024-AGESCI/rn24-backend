import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_profile(logged_api_client, person):
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
        "is_staff": False,
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
    }
