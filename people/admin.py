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
    list_display = ("name", "subdistrict")


@admin.register(Subdistrict)
class SubdistrictAdmin(BaseAdmin):
    list_display = ("name", "district", "scout_groups_count")
    search_fields = ("name",)
    list_filter = ("district",)


@admin.register(District)
class DistrictAdmin(BaseAdmin):
    list_display = ("name", "subdistricts_count", "scout_groups_count")
    search_fields = ("name",)


@admin.register(Squad)
class SquadAdmin(BaseAdmin):
    pass
