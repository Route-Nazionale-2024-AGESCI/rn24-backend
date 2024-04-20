import pytest
from rest_framework.test import APIClient

from people.factories import PersonFactory
from cms.factories import CMSPageFactory


@pytest.fixture(autouse=True)
def use_dummy_storage_backend(settings):
    settings.STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


@pytest.fixture
def person():
    return PersonFactory()


@pytest.fixture
def logged_api_client(person):
    client = APIClient()
    client.force_authenticate(user=person.user)
    return client


@pytest.fixture
def base_events_page():
    return CMSPageFactory(title="Eventi")
