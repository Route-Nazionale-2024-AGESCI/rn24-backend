from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from wagtail.models import Locale, Page, Site

from cms.models.page import CMSPage


class Command(BaseCommand):
    help = "re-create Wagtail Root pages"

    def handle(self, *args, **options):
        # Get the content type for the Page model
        page_content_type = ContentType.objects.get(app_label="wagtailcore", model="page")

        root_page = Page.objects.order_by("id").first()

        default_locale = Locale.objects.first()

        if not CMSPage.objects.filter(slug="rn24-root").exists():
            home_page = CMSPage(
                slug="rn24-root",
                title="RN24",
                body="",
                locale_id=default_locale.id,
                content_type=page_content_type,
            )
            root_page.add_child(instance=home_page)
        home_page_page = Page.objects.get(slug="rn24-root")

        if not CMSPage.objects.filter(slug="rn24-events-root").exists():

            events_root_page = CMSPage(
                slug="rn24-events-root",
                title="Eventi",
                body="eventi",
                locale_id=default_locale.id,
                content_type=page_content_type,
            )
            # Refresh the home page instance, this Must be a PageInstance for the next step to work
            home_page_page = Page.objects.get(slug="rn24-root")
            home_page_page.add_child(instance=events_root_page)

        if not CMSPage.objects.filter(slug="rn24-squads-root").exists():

            events_root_page = CMSPage(
                slug="rn24-squads-root",
                title="Pattuglie",
                body="pattuglie",
                locale_id=default_locale.id,
                content_type=page_content_type,
            )
            # Refresh the home page instance, this Must be a PageInstance for the next step to work
            home_page_page = Page.objects.get(slug="rn24-root")
            home_page_page.add_child(instance=events_root_page)

        # Create a site with the new homepage set as the root
        # Site.objects.create(hostname="localhost", root_page=home_page, is_default_site=True)
        Site.objects.get_or_create(
            site_name="RN24",
            defaults=dict(hostname="localhost", root_page=home_page_page, is_default_site=True),
        )
