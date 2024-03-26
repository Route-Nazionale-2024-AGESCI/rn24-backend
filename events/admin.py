from django.contrib import admin

from events.models.event import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "starts_at", "ends_at", "kind", "is_registration_required")
    list_filter = ("kind", "is_registration_required")
    search_fields = ("name",)
