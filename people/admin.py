from django.contrib import admin
from django.contrib.admin.models import DELETION, LogEntry
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe

from common.admin import BaseAdmin
from common.pdf import html_to_pdf
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
        "scout_group__name",
    )
    list_display = (
        "agesci_id",
        "first_name",
        "last_name",
        "scout_group_link",
        "squads_list",
        "is_arrived",
    )
    list_filter = (
        "is_arrived",
        "scout_group__subdistrict__district",
        "scout_group__subdistrict",
        "scout_group__happiness_path",
        "squads",
    )
    filter_horizontal = ("squads",)
    autocomplete_fields = ("user", "scout_group")
    readonly_fields = [
        "is_arrived",
        "arrived_at",
        "badge_url",
    ]
    actions = ["mark_as_arrived", "revert_arrival", "print_badge"]

    @admin.display(description="Gruppo scout")
    def scout_group_link(self, obj):
        if not obj.scout_group:
            return None
        url = reverse("admin:people_scoutgroup_change", args=[obj.scout_group.id])
        link = f'<a href="{url}">{obj.scout_group.name}</a>'
        return mark_safe(link)

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
    list_filter = ("is_arrived", "region", "subdistrict", "happiness_path")
    search_fields = ("name", "zone", "region")
    inlines = [PersonInline]
    readonly_fields = [
        "district",
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


class SquadPersonInline(admin.TabularInline):
    model = Person.squads.through
    fields = ("person",)
    autocomplete_fields = ("person",)
    extra = 0


@admin.register(Squad)
class SquadAdmin(BaseAdmin):
    list_display = ("name", "description", "people_count")
    search_fields = ("name", "description")
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
