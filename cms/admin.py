from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from cms.models.page import CMSPage


@admin.register(CMSPage)
class CMSPageAdmin(admin.ModelAdmin):
    search_fields = ["uuid", "title"]
    readonly_fields = [
        "uuid",
        "qr_link",
    ]

    @admin.display(description="QR code")
    def qr_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">QR</a>',
            reverse("page-qr-detail", kwargs={"uuid": obj.uuid}),
        )
