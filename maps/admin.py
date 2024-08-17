from django.contrib.gis import admin

from common.admin import BaseAdmin
from maps.models.location import Location
from maps.models.location_category import LocationCategory


@admin.register(Location)
class LocationAdmin(BaseAdmin, admin.GISModelAdmin):
    gis_widget_kwargs = {
        "attrs": {"default_lat": 45.425580, "default_lon": 11.035253, "default_zoom": 14}
    }
    list_display = ("id", "name", "is_public", "category", "district")
    search_fields = ("uuid", "name", "category__name")
    list_filter = ("is_public", "category", "district")
    list_editable = (
        "name",
        "is_public",
    )


@admin.register(LocationCategory)
class LocationCategoryAdmin(BaseAdmin):
    list_display = ("name", "icon", "icon_html")
    readonly_fields = ("icon_html",)
    search_fields = ("name", "icon")
