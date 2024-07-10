from typing import Any

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

from common.pdf import html_to_pdf
from people.models.person import Person
from settings.models.setting import Setting


class BadgeMixin:
    template_name = "badge_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["person_list"] = [get_object_or_404(Person, uuid=kwargs["uuid"])]
        context["badge_extra_css"] = Setting.get("BADGE_EXTRA_CSS")
        return context


@method_decorator(staff_member_required, name="dispatch")
class BadgeDetailView(BadgeMixin, TemplateView):
    pass


@method_decorator(staff_member_required, name="dispatch")
class BadgeDetailPDFView(BadgeMixin, TemplateView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super().get(request, *args, **kwargs)
        response.render()
        pdf_bytes = html_to_pdf(response.content)
        return HttpResponse(pdf_bytes, content_type="application/pdf")
