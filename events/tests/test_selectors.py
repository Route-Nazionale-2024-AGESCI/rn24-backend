import pytest

from events.factories import EventFactory
from events.services.selectors import get_persons_registered_to_event
from people.factories import PersonFactory


@pytest.fixture
def event():
    return EventFactory()


@pytest.fixture
def person():
    return PersonFactory()


@pytest.fixture
def event_with_person(event, person):
    event.registered_persons.add(person)
    return event


@pytest.mark.django_db
def test_selector__get_persons_registered_to_event(event_with_person, person):
    qs = get_persons_registered_to_event(event_with_person)
    assert len(qs) == 1
    assert qs.first() == person
