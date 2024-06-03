from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from wagtail.models import Site

from api.views.pages.serializers import PageDetailSerializer, PageWithVersionSerializer
from cms.models.page import CMSPage


@extend_schema_view(get=extend_schema(operation_id="api_v1_pages_list"))
class PageListView(generics.RetrieveAPIView):
    serializer_class = PageWithVersionSerializer

    def get_object(self):
        return {
            "version": CMSPage.get_last_updated_timestamp(),
            "data": CMSPage.objects.live().filter(id__in=Site.objects.all().values("root_page")),
        }


class PageDetailView(generics.RetrieveAPIView):
    serializer_class = PageDetailSerializer
    queryset = CMSPage.objects.live().all()
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class PageQRDetailView(PageDetailView):
    def get(self, request, *args, **kwargs):
        # response = super().get(request, *args, **kwargs)
        return HttpResponse(self.get_object().qr_png(), content_type="image/png")
