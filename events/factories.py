import factory
from factory.django import DjangoModelFactory
from wagtail.models import Page

from events.models import Event


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Faker("word")
    page = factory.SubFactory(
        "cms.factories.CMSPageFactory",
        title=factory.SelfAttribute("..name"),
        parent=Page.objects.get(
            slug="rn24-events-root",
        ),
    )
    location = factory.SubFactory("maps.factories.LocationFactory")
    is_registration_required = False
    registration_limit = 10
    starts_at = factory.Faker("date_time")
    ends_at = factory.Faker("date_time")
    kind = "ALTRO"
