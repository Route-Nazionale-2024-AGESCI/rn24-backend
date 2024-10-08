import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory

from people.models import (
    HAPPINESS_PATH_CHOICES,
    ITALIAN_REGION_CHOICES,
    District,
    Person,
    ScoutGroup,
    Squad,
    Subdistrict,
)
from people.models.line import Line

User = get_user_model()


class DistrictFactory(DjangoModelFactory):
    class Meta:
        model = District

    name = factory.Faker("city")
    location = factory.SubFactory(
        "maps.factories.LocationFactory",
        name=factory.SelfAttribute("..name"),
    )


class SubdistrictFactory(DjangoModelFactory):
    class Meta:
        model = Subdistrict

    name = factory.Faker("city")
    district = factory.SubFactory("people.factories.DistrictFactory")
    location = factory.SubFactory(
        "maps.factories.LocationFactory",
        name=factory.SelfAttribute("..name"),
    )


class LineFactory(DjangoModelFactory):
    class Meta:
        model = Line

    name = factory.Faker("city")
    subdistrict = factory.SubFactory("people.factories.SubdistrictFactory")
    location = factory.SubFactory(
        "maps.factories.LocationFactory",
        name=factory.SelfAttribute("..name"),
    )


class ScoutGroupFactory(DjangoModelFactory):
    class Meta:
        model = ScoutGroup

    class Params:
        city = factory.Faker("city")
        number = factory.Faker("pyint", min_value=1, max_value=250)

    @factory.lazy_attribute
    def name(self):
        return self.city.upper() + " " + str(self.number)

    agesci_id = factory.Faker("uuid4")
    zone = factory.Faker("administrative_unit")
    region = factory.Faker("random_element", elements=[x[0] for x in ITALIAN_REGION_CHOICES])
    line = factory.SubFactory(LineFactory)
    happiness_path = factory.Faker(
        "random_element", elements=[x[0] for x in HAPPINESS_PATH_CHOICES]
    )
    arrived_at = None


class SquadFactory(DjangoModelFactory):
    class Meta:
        model = Squad

    name = factory.Faker("word")
    description = factory.Faker("sentence")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    agesci_id = factory.Faker("pyint", min_value=10000000, max_value=99999999)
    user = factory.SubFactory(
        UserFactory,
        username=factory.SelfAttribute("..email"),
        email=factory.SelfAttribute("..email"),
        first_name=factory.SelfAttribute("..first_name"),
        last_name=factory.SelfAttribute("..last_name"),
    )
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    scout_group = factory.SubFactory(ScoutGroupFactory)
