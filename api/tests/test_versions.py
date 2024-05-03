import pytest
from django.urls import reverse
from rest_framework.fields import DateTimeField

from cms.factories import CMSPageFactory
from events.factories import EventFactory
from maps.factories import LocationFactory


@pytest.mark.django_db
def test_get_versions(logged_api_client, root_page):
    url = reverse("version-list")
    page = CMSPageFactory(parent=root_page)
    page.save_revision().publish()
    event = EventFactory()
    location = LocationFactory()
    response = logged_api_client.get(url)
    assert response.status_code == 200, response.content
    assert response.json() == [
        {
            "name": "pages",
            "url": reverse("page-list"),
            "version": DateTimeField().to_representation(event.page.updated_at),
        },
        {
            "name": "events",
            "url": reverse("event-list"),
            "version": DateTimeField().to_representation(event.updated_at),
        },
        {
            "name": "locations",
            "url": reverse("location-list"),
            "version": DateTimeField().to_representation(location.updated_at),
        },
    ]
