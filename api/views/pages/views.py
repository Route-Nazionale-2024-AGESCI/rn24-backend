from django.http import HttpResponse
from django.test import RequestFactory
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.fields import DateTimeField
from rest_framework.response import Response
from wagtail.models import Site

from api.views.pages.serializers import PageDetailSerializer
from cms.models.page import CMSPage


def get_tree_structure():
    root = CMSPage.objects.live().filter(id__in=Site.objects.all().values("root_page")).first()
    tree = CMSPage.dump_bulk(root)
    pages = {x.id: x for x in CMSPage.objects.all()}
    request = RequestFactory()
    request.headers = {}
    request.META = {}

    def navigate_tree(node, parent=None):
        el = pages[node["id"]]
        children = []
        for child in node.get("children", []):
            children.append(navigate_tree(child, parent=el.uuid))
        parent_link = f'<Link to="/pages/{parent}">{el.title}</Link>' if parent else ""
        children_link = [
            f'<Link to="/pages/{child["uuid"]}">{child["title"]}</Link>' for child in children
        ]
        return {
            "uuid": el.uuid,
            "created_at": DateTimeField().to_representation(el.created_at),
            "title": el.title,
            "slug": el.slug,
            "show_in_menus": el.show_in_menus,
            "parent": parent,
            "body": el.serve(request=request).render().content,
            "parent_link": parent_link,
            "children_link": children_link,
            "children": children,
        }

    return [navigate_tree(tree[0])]


@extend_schema_view(get=extend_schema(operation_id="api_v1_pages_list"))
class PageListView(generics.RetrieveAPIView):

    def get_object(self):
        return {
            "version": DateTimeField().to_representation(CMSPage.get_last_updated_timestamp()),
            "data": get_tree_structure(),
        }

    def retrieve(self, request, *args, **kwargs):
        data = self.get_object()
        return Response(data)


class PageDetailView(generics.RetrieveAPIView):
    serializer_class = PageDetailSerializer
    queryset = CMSPage.objects.live().all()
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class PageQRDetailView(PageDetailView):
    def get(self, request, *args, **kwargs):
        return HttpResponse(self.get_object().qr_png(), content_type="image/png")
