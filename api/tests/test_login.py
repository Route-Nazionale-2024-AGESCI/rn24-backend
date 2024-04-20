import pytest
from people.factories import PersonFactory
from django.urls import reverse


@pytest.fixture(autouse=True)
def use_dummy_storage_backend(settings):
    settings.STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"


@pytest.fixture
def person():
    return PersonFactory()


def test_authentication_is_required(client):
    response = client.get(reverse("profile-detail"))
    assert response.status_code == 403, response.content


@pytest.mark.django_db
def test_token_works(client, person):
    url = reverse("profile-detail")
    response = client.get(url, HTTP_AUTHORIZATION=f"Token {person.user.auth_token}")
    assert response.status_code == 200
