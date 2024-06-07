from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from events.models.event import Event


class PersonEventVisibilityInline(admin.TabularInline):
    model = Event.visibility_to_persons.through
    autocomplete_fields = ("person",)
    extra = 1


class ScoutGroupEventVisibilityInline(admin.TabularInline):
    model = Event.visibility_to_scout_groups.through
    autocomplete_fields = ("scout_group",)
    extra = 1


class LineEventVisibilityInline(admin.TabularInline):
    model = Event.visibility_to_lines.through
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


class LineEventRegistrationInline(admin.TabularInline):
    model = Event.registered_lines.through
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
    date_hierarchy = "starts_at"
    list_display = (
        "name",
        "location",
        "starts_at",
        "ends_at",
        "kind",
        "personal_registrations_count",
        "is_registration_required",
    )
    list_filter = ("kind", "is_registration_required")
    autocomplete_fields = ("location", "page")
    search_fields = ("uuid", "name", "location__name")
    inlines = (
        PersonEventVisibilityInline,
        ScoutGroupEventVisibilityInline,
        LineEventVisibilityInline,
        SubdistrictEventVisibilityInline,
        DistrictEventVisibilityInline,
        SquadEventVisibilityInline,
        PersonEventRegistrationInline,
        ScoutGroupEventRegistrationInline,
        LineEventRegistrationInline,
        SubdistrictEventRegistrationInline,
        DistrictEventRegistrationInline,
        SquadEventRegistrationInline,
    )

    @admin.display(description="QR code")
    def qr_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">QR</a>',
            reverse("event-qr-detail", kwargs={"uuid": obj.uuid}),
        )

    readonly_fields = (
        "personal_registrations_count",
        "cms_page_link",
        "available_slots",
        "persons_visibility_count",
        "persons_registration_count",
        "qr_link",
    )
