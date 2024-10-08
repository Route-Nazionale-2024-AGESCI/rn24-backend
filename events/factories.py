import factory
from factory.django import DjangoModelFactory

from cms.models.page import CMSPage
from events.models import Event


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Faker("word")
    page = factory.SubFactory(
        "cms.factories.CMSPageFactory",
        title=factory.SelfAttribute("..name"),
        parent=factory.LazyAttribute(
            lambda obj: CMSPage.objects.filter(slug="rn24-events-root").first()
        ),
    )
    location = factory.SubFactory("maps.factories.LocationFactory")
    is_registration_required = False
    registration_limit = 10
    starts_at = factory.Faker("date_time")
    ends_at = factory.Faker("date_time")
    kind = "ALTRO"
