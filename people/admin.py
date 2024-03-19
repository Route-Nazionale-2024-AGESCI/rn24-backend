from django.contrib import admin

from common.admin import BaseAdmin
from people.models.district import District
from people.models.person import Person
from people.models.scout_group import ScoutGroup
from people.models.squad import Squad
from people.models.subdistrict import Subdistrict


@admin.register(Person)
class PersonAdmin(BaseAdmin):
    pass


@admin.register(ScoutGroup)
class ScoutGroupAdmin(BaseAdmin):
    pass


@admin.register(Subdistrict)
class SubdistrictAdmin(BaseAdmin):
    pass


@admin.register(District)
class DistrictAdmin(BaseAdmin):
    pass


@admin.register(Squad)
class SquadAdmin(BaseAdmin):
    pass
