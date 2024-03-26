from django.contrib.gis import admin

from maps.models.location import Location


@admin.register(Location)
class LocationAdmin(admin.GISModelAdmin):
    gis_widget_kwargs = {
        "attrs": {"default_lat": 45.425580, "default_lon": 11.035253, "default_zoom": 14}
    }
    list_display = ("name", "coords", "polygon")
    search_fields = ("name",)
