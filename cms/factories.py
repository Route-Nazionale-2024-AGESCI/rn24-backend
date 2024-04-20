import factory
import wagtail_factories
from factory.django import DjangoModelFactory
from wagtail.models.i18n import Locale

from cms.models import CMSPage


class LocaleFactory(DjangoModelFactory):
    class Meta:
        model = Locale
        django_get_or_create = ("language_code",)

    language_code = "it-IT"


class CMSPageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = CMSPage

    locale = factory.SubFactory(LocaleFactory)
