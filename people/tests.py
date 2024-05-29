import base64
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from people.factories import (
    DistrictFactory,
    PersonFactory,
    ScoutGroupFactory,
    SquadFactory,
    SubdistrictFactory,
)

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
        district = DistrictFactory(name="1")
        subdistrict = SubdistrictFactory(name="2", district=district)
        scout_group = ScoutGroupFactory(name="ANCONA 2", subdistrict=subdistrict)
        person = PersonFactory(
            agesci_id="1234",
            first_name="Mario",
            last_name="Rossi",
            email="mario@example.com",
            phone="1234567890",
            scout_group=scout_group,
            uuid="73e12e83-4ee8-4c1a-9d29-703ab6685c33",
            region="MARCHE",
        )
        squad_1 = SquadFactory(name="pompieri")
        person.squads.add(squad_1)
        squad_2 = SquadFactory(name="sicurezza")
        person.squads.add(squad_2)
        return person

    @pytest.fixture
    def expected_qr_string_base64(self, mario):
        payload_list = "#".join(
            [
                "B",
                f"{mario.uuid}",
                f"{mario.first_name}",
                f"{mario.last_name}",
                f"{mario.email}",
                f"{mario.phone}",
                f"{mario.scout_group.name}",
                f"{mario.region}",
                f"{mario.subdistrict_name()}",
                f"{mario.district_name()}",
                f"{mario.squad_list_string()}",
            ]
        )
        base64_payload = base64.b64encode(payload_list.encode("utf-8")).decode("utf-8")
        return base64_payload

    @pytest.fixture
    def expected_qr_string(self):
        return "B#73e12e83-4ee8-4c1a-9d29-703ab6685c33#Mario#Rossi#mario@example.com#1234567890#ANCONA 2#MARCHE#2#1#pompieri, sicurezza"

    @pytest.mark.django_db
    def test_person_squad_list_to_string(self, mario):
        assert mario.squad_list_string() == "pompieri, sicurezza"

    @pytest.mark.django_db
    def test_person_qr_string(self, mario, expected_qr_string_base64, expected_qr_string):
        assert mario.qr_string() == expected_qr_string_base64
        assert base64.b64decode(mario.qr_string()).decode("utf-8") == expected_qr_string

    @pytest.mark.django_db
    @patch("people.models.person.sign_string", return_value="FOOBAR")
    def test_person_qr_string_with_signature(self, mock, mario, expected_qr_string_base64):
        assert mario.qr_string_with_signature() == expected_qr_string_base64 + "#FOOBAR"
