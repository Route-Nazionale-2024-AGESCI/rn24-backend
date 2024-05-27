from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from people.models.person import Person


@method_decorator(staff_member_required, name="dispatch")
class BadgeDetailView(TemplateView):
    template_name = "badge_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["person"] = get_object_or_404(Person, uuid=kwargs["uuid"])
        return context
