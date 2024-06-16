from django.contrib import admin
from django.db.models import F
from django.urls import reverse
from django.utils.html import format_html

from common.admin import BaseAdmin
from events.models.event import Event
from events.models.event_registration import ScoutGroupEventRegistration


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
    autocomplete_fields = ("line",)
    extra = 1


class SubdistrictEventVisibilityInline(admin.TabularInline):
    model = Event.visibility_to_subdistricts.through
    autocomplete_fields = ("subdistrict",)
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
    autocomplete_fields = ("line",)
    extra = 1


class SubdistrictEventRegistrationInline(admin.TabularInline):
    model = Event.registered_subdistricts.through
    autocomplete_fields = ("subdistrict",)
    extra = 1


class DistrictEventRegistrationInline(admin.TabularInline):
    model = Event.registered_districts.through
    extra = 1


class SquadEventRegistrationInline(admin.TabularInline):
    model = Event.registered_squads.through
    extra = 1


class PersonalRegistrationCountAdminFilter(admin.SimpleListFilter):
    title = "numero di iscrizioni personali"
    parameter_name = "personal_registrations_count"

    def lookups(self, request, model_admin):
        return (
            ("0", "nessuna iscrizione"),
            ("1", "con iscritti"),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        if self.value() == "0":
            return queryset.filter(personal_registrations_count=0)
        if self.value() == "1":
            return queryset.filter(personal_registrations_count__gt=0)


@admin.register(Event)
class EventAdmin(BaseAdmin):
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
    list_filter = ("kind", "is_registration_required", PersonalRegistrationCountAdminFilter)
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


@admin.register(ScoutGroupEventRegistration)
class ScoutGroupEventRegistrationAdmin(BaseAdmin):
    date_hierarchy = "event__starts_at"
    list_display = (
        "event",
        "annotated_event_starts_at",
        "scout_group",
        "check_in",
    )
    list_filter = ("check_in", "event__kind")
    search_fields = (
        "event__uuid",
        "event__name",
        "event__kind",
        "event__location__name",
        "scout_group__name",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            annotated_event_starts_at=F("event__starts_at"),
        )
        return queryset

    @admin.display(description="data inizio", ordering="annotated_event_starts_at")
    def annotated_event_starts_at(self, obj):
        return obj.annotated_event_starts_at
