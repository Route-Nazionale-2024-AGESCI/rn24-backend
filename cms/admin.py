from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from cms.models.page import CMSPage


@admin.register(CMSPage)
class CMSPageAdmin(admin.ModelAdmin):
    search_fields = ["id", "uuid", "title", "slug"]
    readonly_fields = [
        "uuid",
        "qr_link",
        "cms_page_link",
    ]
    list_display = [
        "id",
        "title",
        "slug",
        "cms_page_link",
    ]

    @admin.display(description="QR code")
    def qr_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">QR</a>',
            reverse("page-qr-detail", kwargs={"uuid": obj.uuid}),
        )

    @admin.display(description="modifica la pagina CMS")
    def cms_page_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.get_admin_url(),
            obj.get_admin_url(),
        )
