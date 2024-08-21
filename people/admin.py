from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import DELETION, LogEntry
from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import StringAgg
from django.db.models import F
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

from authentication.services.password import generate_and_send_password
from common.admin import BaseAdmin
from common.pdf import html_to_pdf
from people.models.district import District
from people.models.line import Line
from people.models.person import Person
from people.models.person_check_in import PersonCheckIn
from people.models.scout_group import ScoutGroup
from people.models.squad import Squad
from people.models.subdistrict import Subdistrict
from people.resources import ScoutGroupResource
from people.services.check_in import mark_check_in
from settings.models.setting import Setting

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


class PersonCheckInInlineAdmin(admin.TabularInline):
    model = PersonCheckIn
    show_change_link = True
    fields = readonly_fields = (
        "direction",
        "created_at",
        "user",
    )
    extra = 0

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Person)
class PersonAdmin(BaseAdmin):

    def __init__(self, *args, **kwargs) -> None:
        self.request: HttpRequest | None = None
        super().__init__(*args, **kwargs)

    def get_list_display(self, request: HttpRequest):
        self.request = request
        return super().get_list_display(request)

    # def get_fields(self, request, obj):
    #     all_fields = super().get_fields(request, obj)
    #     return [x for x in all_fields if x not in Person.SENSIBLE_FIELDS]

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
        "full_name",
        "scout_group_link",
        "annotated_squads",
        "line_name",
        "is_arrived",
        "scout_group_has_problems_with_payments",
        "accessibility_has_wheelchair",
        "accessibility_has_caretaker_not_registered",
        "sleeping_is_sleeping_in_tent",
        "sleeping_place",
        "sleeping_tent_name",
        "food_diet_needed",
        "food_is_vegan",
        "transportation_has_problems_moving_on_foot",
        "health_has_allergies",
        "health_has_movement_disorders",
        "health_has_patologies",
        "is_available_for_extra_service",
        "annotated_last_login",
        "impersonate_button",
    )
    list_filter = (
        "is_arrived",
        "scout_group__has_problems_with_payments",
        "scout_group__line__subdistrict__district",
        "squads",
        LastLoginAdminFilter,
        "accessibility_has_wheelchair",
        "accessibility_has_caretaker_not_registered",
        "sleeping_is_sleeping_in_tent",
        "sleeping_place",
        "food_diet_needed",
        "food_is_vegan",
        "transportation_has_problems_moving_on_foot",
        "transportation_need_transport",
        "health_has_allergies",
        "health_has_movement_disorders",
        "health_has_patologies",
        "is_available_for_extra_service",
    )
    filter_horizontal = ("squads",)
    autocomplete_fields = ("user", "scout_group")
    readonly_fields = [
        "is_arrived",
        "arrived_at",
        "badge_url",
        "registered_events_str",
        # "sensible_data_admin_link",
    ]
    actions = [
        "mark_check_in",
        "mark_check_out",
        "print_badge",
        "generate_and_send_password_action",
    ]
    inlines = [
        PersonCheckInInlineAdmin,
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        queryset = super().get_queryset(request)
        queryset = queryset.select_related(
            "user", "scout_group__line__subdistrict__district", "scout_group"
        )
        queryset = queryset.annotate(
            annotated_squads=StringAgg(
                F("squads__name"),
                ", ",
            ),
            annotated_last_login=F("user__last_login"),
        )
        return queryset

    def get_search_results(self, request, queryset, search_term):
        if search_term and " " in search_term and search_term.split(" ").pop().isdigit():
            # se la ricerca finisce con uno spazio ed un numero, allora stiamo cercando un gruppo scout
            print(search_term)
            queryset = queryset.filter(scout_group__name__iexact=search_term)
            return queryset, False
        return super().get_search_results(request, queryset, search_term)

    @admin.display(description="problemi pagamento?", boolean=True)
    def scout_group_has_problems_with_payments(self, obj):
        if obj.scout_group:
            return obj.scout_group.has_problems_with_payments

    @admin.display(description="Ultimo accesso", ordering="annotated_last_login")
    def annotated_last_login(self, obj):
        return obj.annotated_last_login

    @admin.display(description="pattuglie")
    def annotated_squads(self, obj):
        return obj.annotated_squads

    @admin.action(
        permissions=["change"],
        description="Marca ingresso",
    )
    def mark_check_in(self, request, queryset):
        mark_check_in(queryset, "ENTRATA", request.user)

    @admin.action(
        permissions=["change"],
        description="Marca uscita",
    )
    def mark_check_out(self, request, queryset):
        mark_check_in(queryset, "USCITA", request.user)

    @admin.action(
        permissions=["change"],
        description="Genera e invia password",
    )
    def generate_and_send_password_action(self, request, queryset):
        for p in queryset:
            generate_and_send_password(p.user)

    @admin.action(
        description="Stampa badge",
    )
    def print_badge(self, request, queryset):
        html = render_to_string(
            "badge_detail.html",
            {"person_list": queryset, "badge_extra_css": Setting.get("BADGE_EXTRA_CSS")},
        )
        pdf = html_to_pdf(html)
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="badge.pdf"'
        return response

    @admin.display(ordering=None, description="Impersona")
    def impersonate_button(self, obj: Person) -> str:
        if not obj.user:
            return ""
        return format_html(
            '<a href="{}/login?at={}&ct={}" target="_blank">Impersona</a>',
            settings.RN24_FRONTEND_URL,
            obj.user.auth_token.key,
            self.request.META["CSRF_COOKIE"],
        )

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


# @admin.register(SensibleData)
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
        "squads",
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
        "has_problems_with_payments",
        "arrival_date",
        "departure_date",
    )
    list_filter = (
        "is_arrived",
        "has_problems_with_payments",
        "region",
        "line__subdistrict__district",
        "happiness_path",
        ("happiness_path", admin.EmptyFieldListFilter),
    )
    search_fields = ("uuid", "name", "zone", "region")
    inlines = [PersonInline]
    readonly_fields = [
        "district",
        "subdistrict",
        "is_arrived",
        "arrived_at",
        "people_count",
        "children_count",
    ]
    resource_classes = [ScoutGroupResource]


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


@admin.register(Squad)
class SquadAdmin(BaseAdmin):
    list_display = ("name", "description", "people_count")
    search_fields = ("name", "description", "uuid")
    readonly_fields = ("people_count", "cms_page_link")
    filter_horizontal = ("groups",)


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
