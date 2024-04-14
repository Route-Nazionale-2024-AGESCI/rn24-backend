from rest_framework import generics
from wagtail.models import Site

from api.views.pages.serializers import PageDetailSerializer, PageListSerializer
from cms.models.page import CMSPage


class PageListView(generics.ListAPIView):
    serializer_class = PageListSerializer
    queryset = CMSPage.objects.live().filter(id__in=Site.objects.all().values("root_page"))


class PageDetailView(generics.RetrieveAPIView):
    serializer_class = PageDetailSerializer
    queryset = CMSPage.objects.live().all()
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
