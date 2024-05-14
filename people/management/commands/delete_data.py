from django.core.management.base import BaseCommand

from authentication.models.user import User
from cms.models.page import CMSPage
from maps.models.location import Location
from people.models.district import District
from people.models.person import Person
from people.models.scout_group import ScoutGroup
from people.models.squad import Squad
from people.models.subdistrict import Subdistrict


class Command(BaseCommand):
    help = "generate some test data to use for development and testing"

    def handle(self, *args, **options):
        answer = input("Are you sure you want to delete all data? (yes/no): ").lower()
        if answer != "yes":
            return
        print(District.objects.all().delete())
        print(Subdistrict.objects.all().delete())
        print(ScoutGroup.objects.all().delete())
        print(Squad.objects.all().delete())
        print(Person.objects.all().delete())
        print(CMSPage.objects.all().delete())
        print(Location.objects.all().delete())
        print(User.objects.filter(is_superuser=False, is_staff=False).delete())
