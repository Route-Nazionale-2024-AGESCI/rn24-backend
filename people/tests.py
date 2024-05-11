import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from people.factories import PersonFactory, SquadFactory

User = get_user_model()


@pytest.fixture
def person():
    return PersonFactory()


@pytest.fixture
def is_staff_permission():
    return Permission.objects.get(codename="is_staff")


@pytest.fixture
def group_backoffice(is_staff_permission):
    group = Group.objects.create(name="backoffice")
    group.permissions.add(is_staff_permission)
    return group


@pytest.fixture
def squad_with_backoffice(group_backoffice):
    squad = SquadFactory()
    squad.groups.add(group_backoffice)
    return squad


@pytest.mark.django_db
def test_normal_person_cannot_access_backoffice(person):
    assert not person.user.has_perm("people.is_staff")


@pytest.mark.django_db
def test_person_added_to_squad_gains_and_loses_permissions(person, squad_with_backoffice):
    assert not person.user.has_perm("people.is_staff")
    person.squads.add(squad_with_backoffice)
    assert User.objects.get(pk=person.user_id).has_perm("people.is_staff")
    assert User.objects.get(pk=person.user_id).is_staff
    person.squads.clear()
    assert not User.objects.get(pk=person.user_id).has_perm("people.is_staff")
    assert not User.objects.get(pk=person.user_id).is_staff
