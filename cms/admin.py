from django.contrib import admin

from cms.models.page import CMSPage


@admin.register(CMSPage)
class CMSPageAdmin(admin.ModelAdmin):
    search_fields = ["title"]
