import random

import factory
from django.contrib.gis.geos import Point
from factory.django import DjangoModelFactory
from factory.fuzzy import BaseFuzzyAttribute

from maps.models import Location


class FuzzyPoint(BaseFuzzyAttribute):
    def fuzz(self):
        return Point(
            random.uniform(10.96, 11.04),
            random.uniform(45.40, 45.45),
        )


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = Location

    name = factory.Faker("word")
    is_public = False
    category = factory.SubFactory("maps.factories.LocationCategoryFactory")
    coords = FuzzyPoint()


class LocationCategoryFactory(DjangoModelFactory):
    class Meta:
        model = "maps.LocationCategory"

    name = factory.Faker("uuid4")
    icon = factory.Faker("word")
