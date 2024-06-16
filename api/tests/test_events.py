import uuid
from datetime import timedelta

import pytest
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.utils import timezone
from rest_framework.fields import DateTimeField

from events.factories import EventFactory
from events.models import (
    PersonEventRegistration,
    PersonEventVisibility,
    ScoutGroupEventRegistration,
)
from events.models.event import Event
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
        event.refresh_from_db()
        assert event.personal_registrations_count == 1

    @pytest.mark.django_db
    def test_register_to_event_do_change_version(
        self, logged_api_client, person, base_events_page, url
    ):
        event = EventFactory(
            is_registration_required=True,
            starts_at=timezone.now() + timedelta(days=1),
        )
        event_version_before = Event.get_last_updated_timestamp()
        PersonEventVisibility.objects.create(person=person, event=event)
        response = logged_api_client.post(url, {"event": str(event.uuid)})
        assert response.status_code == 201, response.content
        event_version_after = Event.get_last_updated_timestamp()
        assert event_version_before != event_version_after

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
        initial_registration_count = event.personal_registrations_count
        PersonEventRegistration.objects.create(person=person, event=event)
        PersonEventVisibility.objects.create(person=person, event=event)
        response = logged_api_client.post(url, {"event": str(event.uuid)})
        assert response.status_code == 400, response.content
        assert response.json() == [RegistrationErrors.ALREADY_REGISTERED]
        event.refresh_from_db()
        assert event.personal_registrations_count == initial_registration_count

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

    @pytest.mark.django_db
    def test_register_to_multiple_events_of_same_module(
        self, logged_api_client, person, base_events_page, url
    ):
        event_1 = EventFactory(
            is_registration_required=True,
            starts_at=timezone.now() + timedelta(days=1),
            kind="SGUARDI",
        )
        event_2 = EventFactory(
            is_registration_required=True,
            starts_at=timezone.now() + timedelta(days=1),
            kind="SGUARDI",
        )
        PersonEventRegistration.objects.create(person=person, event=event_1)
        PersonEventVisibility.objects.create(person=person, event=event_2)
        response = logged_api_client.post(url, {"event": str(event_2.uuid)})
        assert response.status_code == 400, response.content
        assert response.json() == [RegistrationErrors.ALREADY_REGISTERED_TO_SAME_KIND]
        assert not PersonEventRegistration.objects.filter(person=person, event=event_2).exists()


class TestDeleteRegistration:

    @pytest.fixture
    def url_name(self):
        return "event-registration-detail"

    @pytest.mark.django_db
    def test_delete_registration__ok(self, logged_api_client, person, base_events_page, url_name):
        event = EventFactory(personal_registrations_count=4)
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
        event.refresh_from_db()
        assert event.personal_registrations_count == 3


@pytest.mark.django_db
def test_get_events(logged_api_client, base_events_page):
    event_1 = EventFactory(starts_at=timezone.now())
    event_2 = EventFactory(starts_at=timezone.now() + timedelta(1))
    url = reverse("event-list")
    response = logged_api_client.get(url)
    assert response.status_code == 200, response.content
    assert len(response.json()["data"]) == 2
    assert response.json() == {
        "version": DateTimeField().to_representation(event_2.updated_at),
        "data": [
            {
                "created_at": DateTimeField().to_representation(event_1.created_at),
                "ends_at": DateTimeField().to_representation(event_1.ends_at),
                "is_registration_required": event_1.is_registration_required,
                "kind": event_1.kind,
                "location": str(event_1.location.uuid),
                "name": event_1.name,
                "page": str(event_1.page.uuid),
                "registration_limit": event_1.registration_limit,
                "registration_limit_from_same_scout_group": event_1.registration_limit_from_same_scout_group,
                "personal_registrations_count": 0,
                "registrations_close_at": None,
                "registrations_open_at": None,
                "starts_at": DateTimeField().to_representation(event_1.starts_at),
                "uuid": str(event_1.uuid),
                "id": event_1.id,
                "happiness_path": event_1.happiness_path,
                "correlation_id": event_1.correlation_id,
            },
            {
                "created_at": DateTimeField().to_representation(event_2.created_at),
                "ends_at": DateTimeField().to_representation(event_2.ends_at),
                "is_registration_required": event_2.is_registration_required,
                "kind": event_2.kind,
                "location": str(event_2.location.uuid),
                "name": event_2.name,
                "page": str(event_2.page.uuid),
                "registration_limit": event_2.registration_limit,
                "registration_limit_from_same_scout_group": event_2.registration_limit_from_same_scout_group,
                "personal_registrations_count": 0,
                "registrations_close_at": None,
                "registrations_open_at": None,
                "starts_at": DateTimeField().to_representation(event_2.starts_at),
                "uuid": str(event_2.uuid),
                "id": event_2.id,
                "happiness_path": event_2.happiness_path,
                "correlation_id": event_2.correlation_id,
            },
        ],
    }


@pytest.mark.django_db
def test_get_events_ordered_by_start_date(logged_api_client, base_events_page):
    event_1 = EventFactory(starts_at=timezone.now() + timedelta(days=2))
    event_2 = EventFactory(starts_at=timezone.now() + timedelta(days=1))
    url = reverse("event-list")
    response = logged_api_client.get(url)
    assert response.status_code == 200, response.content
    assert len(response.json()["data"]) == 2
    assert response.json()["data"][0]["uuid"] == str(event_2.uuid)
    assert response.json()["data"][1]["uuid"] == str(event_1.uuid)


class TestEventAttendee:
    @pytest.fixture
    def url(self, event):
        return reverse("event-attendees-list", kwargs={"uuid": event.uuid})

    @pytest.fixture
    def attendee(self):
        return PersonFactory()

    @pytest.fixture
    def event(self, attendee):
        event = EventFactory()
        event.registered_persons.add(attendee)
        return event

    @pytest.mark.django_db
    def test_get_attendees__no_permission(self, logged_api_client, url):
        response = logged_api_client.get(url)
        assert response.status_code == 403, response.content

    @pytest.mark.django_db
    def test_get_attendees__ok(self, logged_api_client, url, person, attendee):
        permission = Permission.objects.get(codename="can_scan_qr")
        person.user.user_permissions.add(permission)
        response = logged_api_client.get(url)
        assert response.status_code == 200, response.content
        assert len(response.json()) == 1
        assert response.json()[0]["uuid"] == str(attendee.uuid)


class TestEventCheckIn:

    @pytest.fixture
    def event(self):
        return EventFactory()

    @pytest.fixture
    def event_with_registered_scout_group(self, event, person):
        ScoutGroupEventRegistration.objects.create(event=event, scout_group=person.scout_group)
        return event

    @pytest.fixture
    def event_with_registered_scout_group_check_in_done(self, event, person):
        ScoutGroupEventRegistration.objects.create(
            event=event, scout_group=person.scout_group, check_in=True
        )
        return event

    @pytest.fixture
    def url(self, event):
        return reverse("event-check-in-detail", kwargs={"uuid": event.uuid})

    @pytest.mark.django_db
    def test_event_check_in(self, logged_api_client, url, event_with_registered_scout_group):
        assert (
            ScoutGroupEventRegistration.objects.filter(event=event_with_registered_scout_group)
            .first()
            .check_in
            is False
        )
        response = logged_api_client.post(url)
        assert response.status_code == 201, response.content
        assert response.json() == {}
        assert (
            ScoutGroupEventRegistration.objects.filter(event=event_with_registered_scout_group)
            .first()
            .check_in
            is True
        )

    @pytest.mark.django_db
    def test_event_check_in_idempotent(
        self, logged_api_client, url, event_with_registered_scout_group_check_in_done
    ):
        response = logged_api_client.post(url)
        assert response.status_code == 201, response.content
        assert (
            ScoutGroupEventRegistration.objects.filter(
                event=event_with_registered_scout_group_check_in_done, check_in=True
            ).exists()
            is True
        )

    @pytest.mark.django_db
    def test_event_check_in_not_registered(self, logged_api_client, url, event):
        response = logged_api_client.post(url)
        assert response.status_code == 404, response.content
        assert ScoutGroupEventRegistration.objects.filter(event=event).exists() is False

    @pytest.mark.django_db
    def test_event_get_check_in_done(
        self, logged_api_client, url, event_with_registered_scout_group_check_in_done
    ):
        response = logged_api_client.get(url)
        assert response.status_code == 200, response.content
        assert response.json() == {"check_in": True}

    @pytest.mark.django_db
    def test_event_get_check_in_not_done(
        self, logged_api_client, url, event_with_registered_scout_group
    ):
        response = logged_api_client.get(url)
        assert response.status_code == 200, response.content
        assert response.json() == {"check_in": False}

    @pytest.mark.django_db
    def test_event_get_for_event_not_registered(self, logged_api_client, url, event):
        response = logged_api_client.get(url)
        assert response.status_code == 404, response.content

    @pytest.mark.django_db
    def test_event_checkin_delete__ok(
        self, logged_api_client, url, event_with_registered_scout_group_check_in_done
    ):
        assert ScoutGroupEventRegistration.objects.filter(
            event=event_with_registered_scout_group_check_in_done, check_in=True
        ).exists()
        response = logged_api_client.delete(url)
        assert response.status_code == 204, response.content
        assert not ScoutGroupEventRegistration.objects.filter(
            event=event_with_registered_scout_group_check_in_done, check_in=True
        ).exists()

    @pytest.mark.django_db
    def test_event_checkin_delete__not_registered(self, logged_api_client, url, event):
        assert not ScoutGroupEventRegistration.objects.filter(event=event, check_in=True).exists()
        response = logged_api_client.delete(url)
        assert response.status_code == 404, response.content
        assert not ScoutGroupEventRegistration.objects.filter(event=event, check_in=True).exists()

    @pytest.mark.django_db
    def test_event_checkin_delete__not_checked_in_is_idempotent(
        self, logged_api_client, url, event_with_registered_scout_group
    ):
        assert not ScoutGroupEventRegistration.objects.filter(
            event=event_with_registered_scout_group, check_in=True
        ).exists()
        response = logged_api_client.delete(url)
        assert response.status_code == 204, response.content
        assert not ScoutGroupEventRegistration.objects.filter(
            event=event_with_registered_scout_group, check_in=True
        ).exists()
