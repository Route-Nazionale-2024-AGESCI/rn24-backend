from django.contrib import admin

from events.models.event import Event


class PersonEventVisibilityInline(admin.TabularInline):
    model = Event.visibility_to_persons.through
    autocomplete_fields = ("person",)
    extra = 1


class ScoutGroupEventVisibilityInline(admin.TabularInline):
    model = Event.visibility_to_scout_groups.through
    autocomplete_fields = ("scout_group",)
    extra = 1


class SubdistrictEventVisibilityInline(admin.TabularInline):
    model = Event.visibility_to_subdistricts.through
    extra = 1


class DistrictEventVisibilityInline(admin.TabularInline):
    model = Event.visibility_to_districts.through
    extra = 1


class SquadEventVisibilityInline(admin.TabularInline):
    model = Event.visibility_to_squads.through
    extra = 1


class PersonEventRegistrationInline(admin.TabularInline):
    model = Event.registered_persons.through
    autocomplete_fields = ("person",)
    extra = 1


class ScoutGroupEventRegistrationInline(admin.TabularInline):
    model = Event.registered_scout_groups.through
    autocomplete_fields = ("scout_group",)
    extra = 1


class SubdistrictEventRegistrationInline(admin.TabularInline):
    model = Event.registered_subdistricts.through
    extra = 1


class DistrictEventRegistrationInline(admin.TabularInline):
    model = Event.registered_districts.through
    extra = 1


class SquadEventRegistrationInline(admin.TabularInline):
    model = Event.registered_squads.through
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "starts_at", "ends_at", "kind", "is_registration_required")
    list_filter = ("kind", "is_registration_required")
    search_fields = ("name",)
    inlines = (
        PersonEventVisibilityInline,
        ScoutGroupEventVisibilityInline,
        SubdistrictEventVisibilityInline,
        DistrictEventVisibilityInline,
        SquadEventVisibilityInline,
        PersonEventRegistrationInline,
        ScoutGroupEventRegistrationInline,
        SubdistrictEventRegistrationInline,
        DistrictEventRegistrationInline,
        SquadEventRegistrationInline,
    )
    readonly_fields = (
        "cms_page_link",
        "available_slots",
        "persons_visibility_count",
        "persons_registration_count",
    )
