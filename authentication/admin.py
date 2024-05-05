from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = BaseUserAdmin.readonly_fields + ("person_admin_link",)
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Profile",
            {"fields": ("person_admin_link",)},
        ),
    )
