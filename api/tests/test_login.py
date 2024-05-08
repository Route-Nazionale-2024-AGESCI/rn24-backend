from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from authentication.AGESCI import AGESCILoginClient
from events.factories import EventFactory
from events.models.event_visibility import PersonEventVisibility


def test_authentication_is_required(client):
    response = client.get(reverse("profile-detail"))
    assert response.status_code == 403, response.content


@pytest.mark.django_db
def test_token_works(client, person):
    url = reverse("profile-detail")
    response = client.get(url, HTTP_AUTHORIZATION=f"Token {person.user.auth_token}")
    assert response.status_code == 200


@pytest.mark.django_db
class TestLoginView:

    @pytest.fixture
    def agesci_token_request(self, requests_mock):
        requests_mock.post(
            AGESCILoginClient.access_token_url,
            status_code=200,
            json={"access_token": "12345"},
        )
        return requests_mock

    @pytest.fixture
    def agesci_success(self, agesci_token_request):
        agesci_token_request.post(
            AGESCILoginClient.login_url,
            status_code=200,
            json={"username": "foo"},
        )

    @pytest.fixture
    def agesci_failure(self, agesci_token_request):
        agesci_token_request.post(
            AGESCILoginClient.login_url,
            status_code=400,
        )

    def test_login(self, client, person_without_user, agesci_success):
        url = reverse("login")
        data = {"username": person_without_user.agesci_id, "password": "QWERTY"}
        response = client.post(url, data)
        assert response.status_code == 201, response.content
        assert "token" in response.json()
        person_without_user.refresh_from_db()
        assert person_without_user.user is not None
        assert response.json() == {
            "token": person_without_user.user.auth_token.key,
            "csrftoken": response.cookies["csrftoken"].value,
        }

    def test_login_wrong_password(self, client, person_without_user, agesci_failure):
        url = reverse("login")
        data = {"username": person_without_user.agesci_id, "password": "wrong"}
        response = client.post(url, data)
        assert response.status_code == 403
        person_without_user.refresh_from_db()
        assert person_without_user.user is None

    def test_login_wrong_username(self, client, person_without_user, agesci_failure):
        url = reverse("login")
        data = {"username": "wrong", "password": "password"}
        response = client.post(url, data)
        assert response.status_code == 403
        person_without_user.refresh_from_db()
        assert person_without_user.user is None

    def test_login_fallback_to_django_user(self, client, person, agesci_failure):
        person.user.set_password("password")
        person.user.save()
        url = reverse("login")
        data = {"username": person.user.username, "password": "password"}
        response = client.post(url, data)
        assert response.status_code == 201, response.content
        assert "token" in response.json()
        assert response.json()["token"] == person.user.auth_token.key

    def test_login_x_csrf_token(self, person_without_user, agesci_success):
        api_client = APIClient(enforce_csrf_checks=True)
        url = reverse("login")
        data = {"username": person_without_user.agesci_id, "password": "QWERTY"}
        response = api_client.post(url, data)
        assert response.status_code == 201, response.content
        token = response.json()["token"]
        csrf_token = response.cookies["csrftoken"].value

        event = EventFactory(
            is_registration_required=True,
            starts_at=timezone.now() + timedelta(days=1),
        )
        PersonEventVisibility.objects.create(person=person_without_user, event=event)
        # this fails because we don't send CSRF token
        response = api_client.post(reverse("event-registration-list"), {"event": str(event.uuid)})
        assert response.status_code == 403, response.content
        assert response.json() == {"detail": "CSRF Failed: CSRF token missing."}
        # now we send the CSRF token as an HTTP header and it works
        response = api_client.post(
            reverse("event-registration-list"),
            {"event": str(event.uuid)},
            HTTP_X_CSRFTOKEN=csrf_token,
            HTTP_AUTHORIZATION=f"Token {token}",
        )
        assert response.status_code == 201, response.content
