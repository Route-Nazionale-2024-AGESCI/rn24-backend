from django.contrib import admin
from django.utils.html import format_html


class CMSPageLinkMixin:
    @admin.display(description="modifica la pagina CMS dell'evento")
    def cms_page_link(self):
        if not self.page:
            return None
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            self.page.get_admin_url(),
            self.page.get_admin_url(),
        )
