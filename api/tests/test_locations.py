import pytest
from django.urls import reverse
from rest_framework.fields import DateTimeField

from maps.factories import LocationFactory


@pytest.mark.django_db
def test_get_locations(logged_api_client):
    url = reverse("location-list")
    location = LocationFactory()
    response = logged_api_client.get(url)
    assert response.status_code == 200
    assert response.json() == [
        {
            "coords": {
                "coordinates": [
                    location.coords.x,
                    location.coords.y,
                ],
                "type": "Point",
            },
            "created_at": DateTimeField().to_representation(location.created_at),
            "name": location.name,
            "polygon": None,
            "uuid": str(location.uuid),
        },
    ]
