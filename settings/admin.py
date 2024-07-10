from django.contrib.gis import admin

from common.admin import BaseAdmin
from settings.models.setting import Setting


@admin.register(Setting)
class SettingAdmin(BaseAdmin):
    list_display = ("id", "key", "value")
    list_editable = ("key", "value")
