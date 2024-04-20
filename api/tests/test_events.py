import uuid
from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.fields import DateTimeField

from events.factories import EventFactory
from events.models import (
    PersonEventRegistration,
    PersonEventVisibility,
    ScoutGroupEventRegistration,
)
from events.services.registration import RegistrationErrors
from people.factories import PersonFactory


@pytest.mark.django_db
def test_get_registrations(logged_api_client, person, base_events_page):
    event_personal = EventFactory()
    event_group = EventFactory()
    PersonEventRegistration.objects.create(person=person, event=event_personal)
    ScoutGroupEventRegistration.objects.create(scout_group=person.scout_group, event=event_group)

    url = reverse("event-registration-list")
    response = logged_api_client.get(url)
    assert response.status_code == 200, response.content
    assert response.json() == [
        {
            "event": str(event_personal.uuid),
            "is_personal": True,
        },
        {
            "event": str(event_group.uuid),
            "is_personal": False,
        },
    ]


class TestRegisterToEvent:

    @pytest.fixture
    def url(self):
        return reverse("event-registration-list")

    @pytest.mark.django_db
    def test_register_to_event__ok(self, logged_api_client, person, base_events_page, url):
        event = EventFactory(
            is_registration_required=True,
            starts_at=timezone.now() + timedelta(days=1),
        )
        PersonEventVisibility.objects.create(person=person, event=event)
        response = logged_api_client.post(url, {"event": str(event.uuid)})
        assert response.status_code == 201, response.content
        assert response.json() == {"event": str(event.uuid)}
        assert PersonEventRegistration.objects.filter(person=person, event=event).exists()

    @pytest.mark.django_db
    def test_register_to_event__not_exists(self, logged_api_client, person, base_events_page, url):
        event = EventFactory()
        response = logged_api_client.post(url, {"event": str(uuid.uuid4())})
        assert response.status_code == 404, response.content
        assert not PersonEventRegistration.objects.filter(person=person, event=event).exists()

    @pytest.mark.django_db
    def test_register_to_event__registration_not_required(
        self, logged_api_client, person, base_events_page, url
    ):
        event = EventFactory(is_registration_required=False)
        PersonEventVisibility.objects.create(person=person, event=event)
        response = logged_api_client.post(url, {"event": str(event.uuid)})
        assert response.status_code == 400, response.content
        assert response.json() == [RegistrationErrors.NOT_REQUIRED]
        assert not PersonEventRegistration.objects.filter(person=person, event=event).exists()

    @pytest.mark.django_db
    def test_register_to_event__not_invited(self, logged_api_client, person, base_events_page, url):
        event = EventFactory(is_registration_required=False)
        response = logged_api_client.post(url, {"event": str(event.uuid)})
        assert response.status_code == 400, response.content
        assert response.json() == [RegistrationErrors.NOT_VISIBLE]
        assert not PersonEventRegistration.objects.filter(person=person, event=event).exists()

    @pytest.mark.django_db
    def test_register_to_event__event_already_started(
        self, logged_api_client, person, base_events_page, url
    ):
        event = EventFactory(
            is_registration_required=True, starts_at=timezone.now() - timedelta(days=1)
        )
        PersonEventVisibility.objects.create(person=person, event=event)
        response = logged_api_client.post(url, {"event": str(event.uuid)})
        assert response.status_code == 400, response.content
        assert response.json() == [RegistrationErrors.ALREADY_STARTED]
        assert not PersonEventRegistration.objects.filter(person=person, event=event).exists()

    @pytest.mark.django_db
    def test_register_to_event__already_registered(
        self, logged_api_client, person, base_events_page, url
    ):
        event = EventFactory(
            is_registration_required=True,
            starts_at=timezone.now() + timedelta(days=1),
        )
        PersonEventRegistration.objects.create(person=person, event=event)
        PersonEventVisibility.objects.create(person=person, event=event)
        response = logged_api_client.post(url, {"event": str(event.uuid)})
        assert response.status_code == 400, response.content
        assert response.json() == [RegistrationErrors.ALREADY_REGISTERED]

    @pytest.mark.django_db
    def test_register_to_event__full(self, logged_api_client, person, base_events_page, url):
        event = EventFactory(
            is_registration_required=True,
            starts_at=timezone.now() + timedelta(days=1),
            registration_limit=1,
        )
        already_registered_person = PersonFactory()
        PersonEventRegistration.objects.create(person=already_registered_person, event=event)
        PersonEventVisibility.objects.create(person=person, event=event)
        response = logged_api_client.post(url, {"event": str(event.uuid)})
        assert response.status_code == 400, response.content
        assert response.json() == [RegistrationErrors.FULL]
        assert not PersonEventRegistration.objects.filter(person=person, event=event).exists()

    @pytest.mark.django_db
    def test_register_to_event__same_group_limit(
        self, logged_api_client, person, base_events_page, url
    ):
        event = EventFactory(
            is_registration_required=True,
            starts_at=timezone.now() + timedelta(days=1),
            registration_limit=2,
            registration_limit_from_same_scout_group=1,
        )
        already_registered_person = PersonFactory(scout_group=person.scout_group)
        PersonEventRegistration.objects.create(person=already_registered_person, event=event)
        PersonEventVisibility.objects.create(person=person, event=event)
        response = logged_api_client.post(url, {"event": str(event.uuid)})
        assert response.status_code == 400, response.content
        assert response.json() == [RegistrationErrors.SAME_GROUP_LIMIT]
        assert not PersonEventRegistration.objects.filter(person=person, event=event).exists()

    @pytest.mark.django_db
    def test_register_to_event__registrations_not_open_yet(
        self, logged_api_client, person, base_events_page, url
    ):
        event = EventFactory(
            is_registration_required=True,
            starts_at=timezone.now() + timedelta(days=1),
            registrations_open_at=timezone.now() + timedelta(hours=1),
        )
        PersonEventVisibility.objects.create(person=person, event=event)
        response = logged_api_client.post(url, {"event": str(event.uuid)})
        assert response.status_code == 400, response.content
        assert response.json() == [RegistrationErrors.REGISTRATION_NOT_OPEN_YET]
        assert not PersonEventRegistration.objects.filter(person=person, event=event).exists()

    @pytest.mark.django_db
    def test_register_to_event__registrations_already_closed(
        self, logged_api_client, person, base_events_page, url
    ):
        event = EventFactory(
            is_registration_required=True,
            starts_at=timezone.now() + timedelta(days=1),
            registrations_close_at=timezone.now() - timedelta(hours=1),
        )
        PersonEventVisibility.objects.create(person=person, event=event)
        response = logged_api_client.post(url, {"event": str(event.uuid)})
        assert response.status_code == 400, response.content
        assert response.json() == [RegistrationErrors.REGISTRATION_TIME_EXPIRED]
        assert not PersonEventRegistration.objects.filter(person=person, event=event).exists()


class TestDeleteRegistration:

    @pytest.fixture
    def url_name(self):
        return "event-registration-detail"

    @pytest.mark.django_db
    def test_delete_registration__ok(self, logged_api_client, person, base_events_page, url_name):
        event = EventFactory()
        PersonEventRegistration.objects.create(person=person, event=event)
        response = logged_api_client.delete(
            reverse(
                url_name,
                kwargs={"uuid": event.uuid},
            ),
        )
        assert response.status_code == 204, response.content
        assert not response.content
        assert not PersonEventRegistration.objects.filter(person=person, event=event).exists()


@pytest.mark.django_db
def test_get_events(logged_api_client, base_events_page):
    events = EventFactory.create_batch(2)
    url = reverse("event-list")
    response = logged_api_client.get(url)
    assert response.status_code == 200, response.content
    assert len(response.json()) == 2
    assert response.json() == [
        {
            "created_at": DateTimeField().to_representation(events[0].created_at),
            "ends_at": DateTimeField().to_representation(events[0].ends_at),
            "is_registration_required": events[0].is_registration_required,
            "kind": events[0].kind,
            "location": str(events[0].location.uuid),
            "name": events[0].name,
            "page": str(events[0].page.uuid),
            "registration_limit": events[0].registration_limit,
            "registration_limit_from_same_scout_group": events[
                0
            ].registration_limit_from_same_scout_group,
            "registrations_close_at": None,
            "registrations_open_at": None,
            "starts_at": DateTimeField().to_representation(events[0].starts_at),
            "uuid": str(events[0].uuid),
        },
        {
            "created_at": DateTimeField().to_representation(events[1].created_at),
            "ends_at": DateTimeField().to_representation(events[1].ends_at),
            "is_registration_required": events[1].is_registration_required,
            "kind": events[1].kind,
            "location": str(events[1].location.uuid),
            "name": events[1].name,
            "page": str(events[1].page.uuid),
            "registration_limit": events[1].registration_limit,
            "registration_limit_from_same_scout_group": events[
                1
            ].registration_limit_from_same_scout_group,
            "registrations_close_at": None,
            "registrations_open_at": None,
            "starts_at": DateTimeField().to_representation(events[1].starts_at),
            "uuid": str(events[1].uuid),
        },
    ]
