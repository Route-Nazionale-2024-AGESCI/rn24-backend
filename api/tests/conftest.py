import pytest
import wagtail_factories
from rest_framework.test import APIClient
from wagtail.models import Locale

from cms.factories import CMSPageFactory
from people.factories import PersonFactory


@pytest.fixture(autouse=True)
def use_dummy_storage_backend(settings):
    settings.STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


@pytest.fixture
def person():
    return PersonFactory()


@pytest.fixture
def person_without_user():
    return PersonFactory(user=None)


@pytest.fixture
def logged_api_client(person):
    client = APIClient()
    client.force_authenticate(user=person.user)
    return client


@pytest.fixture
def base_events_page():
    return CMSPageFactory(title="Eventi")


@pytest.fixture
def base_squads_page():
    return CMSPageFactory(title="Pattuglie")


@pytest.fixture
def root_page():
    Locale.objects.create(language_code="it")
    root_page = CMSPageFactory()
    root_page.save_revision().publish()
    wagtail_factories.SiteFactory(root_page=root_page)
    return root_page
