from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from people.factories import PersonFactory, ScoutGroupFactory, SquadFactory

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


class TestQR:

    @pytest.fixture
    def mario(self):
        scout_group = ScoutGroupFactory(name="ANCONA 2")
        person = PersonFactory(
            agesci_id="1234",
            first_name="Mario",
            last_name="Rossi",
            email="mario@example.com",
            phone="1234567890",
            scout_group=scout_group,
            uuid="73e12e83-4ee8-4c1a-9d29-703ab6685c33",
        )
        squad_1 = SquadFactory(name="pompieri")
        person.squads.add(squad_1)
        squad_2 = SquadFactory(name="sicurezza")
        person.squads.add(squad_2)
        return person

    @pytest.mark.django_db
    def test_person_squad_list_to_string(self, mario):
        assert mario.squad_list_string() == "pompieri, sicurezza"

    @pytest.mark.django_db
    def test_person_qr_string(self, mario):
        assert (
            mario.qr_string()
            == "B#73e12e83-4ee8-4c1a-9d29-703ab6685c33#Mario#Rossi#mario@example.com#1234567890#ANCONA 2#pompieri, sicurezza"
        )

    @pytest.mark.django_db
    def test_person_qr_string_without_scout_group(self, mario):
        mario.scout_group = None
        mario.save()
        assert (
            mario.qr_string()
            == "B#73e12e83-4ee8-4c1a-9d29-703ab6685c33#Mario#Rossi#mario@example.com#1234567890##pompieri, sicurezza"
        )

    @pytest.mark.django_db
    def test_person_qr_string_without_squads(self, mario):
        mario.squads.clear()
        assert (
            mario.qr_string()
            == "B#73e12e83-4ee8-4c1a-9d29-703ab6685c33#Mario#Rossi#mario@example.com#1234567890#ANCONA 2#"
        )

    @pytest.mark.django_db
    @patch("people.models.person.sign_string", return_value="FOOBAR")
    def test_person_qr_string_with_signature(self, mock, mario):
        assert (
            mario.qr_string_with_signature()
            == "B#73e12e83-4ee8-4c1a-9d29-703ab6685c33#Mario#Rossi#mario@example.com#1234567890#ANCONA 2#pompieri, sicurezza#FOOBAR"
        )
