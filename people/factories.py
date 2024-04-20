from factory.django import DjangoModelFactory
import factory
from people.models import (
    Person,
    ScoutGroup,
    Subdistrict,
    District,
    ITALIAN_REGION_CHOICES,
    HAPPINESS_PATH_CHOICES,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.Faker("password")


class DistrictFactory(DjangoModelFactory):
    class Meta:
        model = District

    name = factory.Faker("city")


class SubdistrictFactory(DjangoModelFactory):
    class Meta:
        model = Subdistrict

    name = factory.Faker("city")
    district = factory.SubFactory("people.factories.DistrictFactory")


class ScoutGroupFactory(DjangoModelFactory):
    class Meta:
        model = ScoutGroup

    class Params:
        city = factory.Faker("city")
        number = factory.Faker("pyint", min_value=1, max_value=250)

    @factory.lazy_attribute
    def name(self):
        return self.city.upper() + " " + str(self.number)

    zone = factory.Faker("administrative_unit")
    region = factory.Faker("random_element", elements=[x[0] for x in ITALIAN_REGION_CHOICES])
    subdistrict = factory.SubFactory("people.factories.SubdistrictFactory")
    happiness_path = factory.Faker(
        "random_element", elements=[x[0] for x in HAPPINESS_PATH_CHOICES]
    )
    arrived_at = None


class PersonFactory(DjangoModelFactory):
    class Meta:
        model = Person

    agesci_id = factory.Faker("pyint", min_value=100000, max_value=999999)
    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    codice_fiscale = factory.Faker("ssn")
    birth_date = factory.Faker("date_of_birth")
    address = factory.Faker("address")
    city = factory.Faker("city")
    scout_group = factory.SubFactory(ScoutGroupFactory)
