import pytest
from django.urls import reverse
from rest_framework.fields import DateTimeField

from maps.factories import LocationFactory
from maps.models.location import Location


def _location_expected_representation(location):
    return {
        "coords": {
            "coordinates": [
                location.coords.x,
                location.coords.y,
            ],
            "type": "Point",
        },
        "created_at": DateTimeField().to_representation(location.created_at),
        "name": location.name,
        "description": location.description,
        "polygon": None,
        "path": None,
        "uuid": str(location.uuid),
        "is_public": location.is_public,
        "category": location.category.name,
        "icon": location.category.icon,
        "color": location.category.color,
        "district": str(location.district.uuid) if location.district else None,
    }


@pytest.mark.django_db
def test_get_locations(logged_api_client):
    url = reverse("location-list")
    location = LocationFactory()
    response = logged_api_client.get(url)
    assert response.status_code == 200
    assert response.json() == {
        "version": DateTimeField().to_representation(location.updated_at),
        "data": [_location_expected_representation(x) for x in Location.objects.all()],
    }
