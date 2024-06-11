from collections.abc import Sequence

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http.request import HttpRequest
from django.utils.html import format_html


from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ("impersonate_button",)
    readonly_fields = BaseUserAdmin.readonly_fields + ("person_admin_link",)
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Profile",
            {"fields": ("person_admin_link",)},
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        self.request: HttpRequest | None = None
        super().__init__(*args, **kwargs)

    def get_list_display(self, request: HttpRequest) -> Sequence[str]:
        self.request = request
        return super().get_list_display(request)

    @admin.display(ordering=None, description="Impersona")
    def impersonate_button(self, obj: User) -> str:
        return format_html(
            '<a href="{}/login?at={}&ct={}" target="_blank">Impersona</a>',
            settings.RN24_FRONTEND_URL,
            obj.auth_token.key,
            self.request.META["CSRF_COOKIE"],
        )
