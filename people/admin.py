from django.contrib import admin
from django.contrib.admin.models import DELETION, LogEntry
from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import StringAgg
from django.db import transaction
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe

from common.admin import BaseAdmin
from common.pdf import html_to_pdf
from people.models.district import District
from people.models.line import Line
from people.models.person import Person
from people.models.scout_group import ScoutGroup
from people.models.sensible_data import SensibleData
from people.models.squad import Squad
from people.models.subdistrict import Subdistrict

User = get_user_model()


class LastLoginAdminFilter(admin.SimpleListFilter):
    title = "Ultimo accesso"
    parameter_name = "last_login"

    def lookups(self, request, model_admin):
        return (
            ("never", "Mai"),
            ("today", "Oggi"),
            ("this_week", "Questa settimana"),
            ("this_month", "Questo mese"),
            ("this_year", "Quest'anno"),
        )

    def queryset(self, request, queryset):
        now = timezone.now()
        if self.value() == "never":
            return queryset.filter(user__last_login__isnull=True)
        if self.value() == "today":
            return queryset.filter(user__last_login__date=now.date())
        if self.value() == "this_week":
            return queryset.filter(user__last_login__week=now.isocalendar()[1])
        if self.value() == "this_month":
            return queryset.filter(user__last_login__month=now.month)
        if self.value() == "this_year":
            return queryset.filter(user__last_login__year=now.year)
        return queryset


@admin.register(Person)
class PersonAdmin(BaseAdmin):

    def get_fields(self, request, obj):
        all_fields = super().get_fields(request, obj)
        return list(set(all_fields) - set(Person.SENSIBLE_FIELDS))

    search_fields = (
        "agesci_id",
        "uuid",
        "first_name",
        "last_name",
        "email",
        "phone",
        "scout_group__name",
    )
    list_display = (
        "agesci_id",
        "first_name",
        "last_name",
        "scout_group_link",
        "annotated_squads",
        "annotated_last_login",
        "is_arrived",
    )
    list_filter = (
        "is_arrived",
        "scout_group__line__subdistrict__district",
        "scout_group__happiness_path",
        "squads",
        LastLoginAdminFilter,
    )
    filter_horizontal = ("squads",)
    autocomplete_fields = ("user", "scout_group")
    readonly_fields = [
        "is_arrived",
        "arrived_at",
        "badge_url",
        "sensible_data_admin_link",
    ]
    actions = ["mark_as_arrived", "revert_arrival", "print_badge"]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            annotated_squads=StringAgg(
                F("squads__name"),
                ", ",
            ),
            annotated_last_login=F("user__last_login"),
        )
        return queryset

    @admin.display(description="Ultimo accesso", ordering="annotated_last_login")
    def annotated_last_login(self, obj):
        return obj.annotated_last_login

    @admin.display(description="pattuglie")
    def annotated_squads(self, obj):
        return obj.annotated_squads

    @admin.action(
        permissions=["change"],
        description="Marca come arrivati",
    )
    def mark_as_arrived(self, request, queryset):
        now = timezone.now()
        with transaction.atomic():
            queryset.filter(is_arrived=False).update(is_arrived=True, arrived_at=now)
            scout_group_qs = ScoutGroup.objects.filter(person__in=queryset).distinct()
            scout_group_qs.filter(is_arrived=False).update(is_arrived=True, arrived_at=now)

    @admin.action(
        permissions=["change"],
        description="Annulla arrivo",
    )
    def revert_arrival(self, request, queryset):
        with transaction.atomic():
            queryset.filter(is_arrived=True).update(is_arrived=False, arrived_at=None)
            scout_group_qs = ScoutGroup.objects.filter(person__in=queryset).distinct()
            for scout_group in scout_group_qs:
                if not scout_group.person_set.filter(is_arrived=True).exists():
                    scout_group.is_arrived = False
                    scout_group.arrived_at = None
                    scout_group.save()

    @admin.action(
        description="Stampa badge",
    )
    def print_badge(self, request, queryset):
        html = render_to_string("badge_detail.html", {"person_list": queryset})
        pdf = html_to_pdf(html)
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="badge.pdf"'
        return response

    def save_model(self, request, obj, form, change):
        if not obj.user:
            if obj.agesci_id:
                username = obj.agesci_id
            else:
                username = obj.email
            obj.user = User.objects.create_user(
                username=username,
                email=obj.email,
                first_name=obj.first_name,
                last_name=obj.last_name,
            )
        super().save_model(request, obj, form, change)


class PersonInline(admin.TabularInline):
    model = Person
    show_change_link = True
    fields = readonly_fields = (
        "agesci_id",
        "first_name",
        "last_name",
        "is_arrived",
    )
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SensibleData)
class SensibleDataAdmin(BaseAdmin):
    search_fields = (
        "agesci_id",
        "uuid",
        "first_name",
        "last_name",
        "email",
        "phone",
        "scout_group__name",
    )
    list_display = [
        "agesci_id",
        "first_name",
        "last_name",
        "scout_group_link",
    ] + Person.SENSIBLE_FIELDS

    list_filter = [
        "accessibility_has_wheelchair",
        "accessibility_has_caretaker_not_registered",
        "sleeping_is_sleeping_in_tent",
        "food_is_vegan",
        "transportation_has_problems_moving_on_foot",
        "health_has_allergies",
        "health_has_movement_disorders",
        "health_has_patologies",
    ]

    def get_fields(self, request, obj):
        all_fields = super().get_fields(request, obj)
        return ["person_admin_link"] + all_fields

    def has_add_permission(self, request, *args, **kwargs):
        return False

    def has_change_permission(self, request, *args, **kwargs):
        return False

    def has_delete_permission(self, request, *args, **kwargs):
        return False


@admin.register(ScoutGroup)
class ScoutGroupAdmin(BaseAdmin):
    list_display = (
        "name",
        "zone",
        "region",
        "line",
        "happiness_path",
        "people_count",
        "is_arrived",
    )
    list_filter = ("is_arrived", "region", "line__subdistrict__district", "happiness_path")
    search_fields = ("uuid", "name", "zone", "region")
    inlines = [PersonInline]
    readonly_fields = [
        "district",
        "subdistrict",
        "is_arrived",
        "arrived_at",
    ]


class ScoutGroupInline(admin.TabularInline):
    model = ScoutGroup
    show_change_link = True
    fields = readonly_fields = (
        "name",
        "zone",
        "region",
        "happiness_path",
        "people_count",
        "is_arrived",
    )
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Line)
class LineAdmin(BaseAdmin):
    list_display = ("name", "subdistrict", "scout_groups_count", "people_count")
    search_fields = ("name", "uuid")
    readonly_fields = ("scout_groups_count", "people_count")
    list_filter = ("subdistrict__district", "subdistrict")
    inlines = [ScoutGroupInline]


class LineInline(admin.TabularInline):
    model = Line
    show_change_link = True
    fields = ("name", "scout_groups_count", "people_count")
    readonly_fields = ("scout_groups_count", "people_count")
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Subdistrict)
class SubdistrictAdmin(BaseAdmin):
    list_display = ("name", "district", "lines_count", "scout_groups_count", "people_count")
    readonly_fields = ("scout_groups_count", "people_count")
    search_fields = ("name", "uuid")
    list_filter = ("district",)
    inlines = [LineInline]


class SubdistrictInline(admin.TabularInline):
    model = Subdistrict
    show_change_link = True
    fields = ("name", "lines_count", "scout_groups_count", "people_count")
    readonly_fields = ("lines_count", "scout_groups_count", "people_count")
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(District)
class DistrictAdmin(BaseAdmin):
    list_display = (
        "name",
        "subdistricts_count",
        "lines_count",
        "scout_groups_count",
        "people_count",
    )
    search_fields = ("name", "uuid")
    readonly_fields = ("subdistricts_count", "scout_groups_count", "people_count")
    inlines = [SubdistrictInline]


class SquadPersonInline(admin.TabularInline):
    model = Person.squads.through
    fields = ("person",)
    autocomplete_fields = ("person",)
    extra = 0


@admin.register(Squad)
class SquadAdmin(BaseAdmin):
    list_display = ("name", "description", "people_count")
    search_fields = ("name", "description", "uuid")
    readonly_fields = ("people_count",)
    filter_horizontal = ("groups",)
    inlines = [SquadPersonInline]


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = "action_time"

    list_filter = ["action_flag", "content_type"]

    search_fields = ["change_message", "object_repr", "user__username"]

    list_display = [
        "action_time",
        "user",
        "content_type",
        "object_link",
        "action_flag",
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    @admin.display(
        description="object",
        ordering="object_repr",
    )
    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="{}">{}</a>'.format(
                reverse(f"admin:{ct.app_label}_{ct.model}_change", args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
