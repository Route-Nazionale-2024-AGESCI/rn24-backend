from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.safestring import mark_safe


class User(AbstractUser):

    @admin.display(description="Persona")
    def person_admin_link(self):
        if not self.person:
            return None
        url = reverse("admin:people_person_change", args=[self.person.id])
        link = f'<a href="{url}">{self.person}</a>'
        return mark_safe(link)
