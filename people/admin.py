from django.contrib import admin

from common.admin import BaseAdmin
from people.models.district import District
from people.models.person import Person
from people.models.scout_group import ScoutGroup
from people.models.squad import Squad
from people.models.subdistrict import Subdistrict


@admin.register(Person)
class PersonAdmin(BaseAdmin):
    search_fields = (
        "agesci_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "codice_fiscale",
        "birth_date",
        "address",
        "city",
        "scout_group__name",
    )
    list_display = ("agesci_id", "first_name", "last_name", "user", "scout_group", "squads_list")
    list_filter = (
        "scout_group__subdistrict__district",
        "scout_group__subdistrict",
        "scout_group__happiness_path",
        "squads",
    )
    filter_horizontal = ("squads",)


class PersonInline(admin.TabularInline):
    model = Person
    show_change_link = True
    fields = readonly_fields = (
        "agesci_id",
        "first_name",
        "last_name",
        "user",
    )
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


class IsArrivedListFilter(admin.SimpleListFilter):
    title = "arrivati?"
    parameter_name = "is_arrived"

    def lookups(self, request, model_admin):
        return [
            ("true", "si"),
            ("false", "no"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "true":
            return queryset.filter(arrived_at__isnull=False)
        if self.value() == "false":
            return queryset.filter(arrived_at__isnull=True)


@admin.register(ScoutGroup)
class ScoutGroupAdmin(BaseAdmin):
    list_display = (
        "name",
        "zone",
        "region",
        "subdistrict",
        "happiness_path",
        "people_count",
        "is_arrived",
    )
    list_filter = ("region", "subdistrict", "happiness_path", IsArrivedListFilter)
    search_fields = ("name", "zone", "region")
    inlines = [PersonInline]


class ScoutGroupInline(admin.TabularInline):
    model = ScoutGroup
    show_change_link = True
    fields = (
        "name",
        "zone",
        "region",
        "subdistrict",
        "happiness_path",
        "people_count",
        "is_arrived",
    )
    readonly_fields = (
        "name",
        "zone",
        "region",
        "subdistrict",
        "happiness_path",
        "people_count",
        "is_arrived",
    )
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Subdistrict)
class SubdistrictAdmin(BaseAdmin):
    list_display = ("name", "district", "scout_groups_count", "people_count")
    readonly_fields = ("scout_groups_count", "people_count")
    search_fields = ("name",)
    list_filter = ("district",)
    inlines = [ScoutGroupInline]


class SubdistrictInline(admin.TabularInline):
    model = Subdistrict
    show_change_link = True
    fields = ("name", "scout_groups_count", "people_count")
    readonly_fields = ("scout_groups_count", "people_count")
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(District)
class DistrictAdmin(BaseAdmin):
    list_display = ("name", "subdistricts_count", "scout_groups_count", "people_count")
    search_fields = ("name",)
    readonly_fields = ("subdistricts_count", "scout_groups_count", "people_count")
    inlines = [SubdistrictInline]


@admin.register(Squad)
class SquadAdmin(BaseAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")
    readonly_fields = ("people_count",)
