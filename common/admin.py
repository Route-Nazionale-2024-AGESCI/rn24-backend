from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = {
            "created_at",
            "updated_at",
            "uuid",
            "deleted_at",
        }
        return readonly_fields.union(set(super().get_readonly_fields(request, obj)))
