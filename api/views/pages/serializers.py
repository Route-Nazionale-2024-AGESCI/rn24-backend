from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from cms.models.page import CMSPage
from common.serializers import UUIDRelatedModelSerializer


class BasePageSerializer(UUIDRelatedModelSerializer):

    body = SerializerMethodField()
    parent = SerializerMethodField()
    parent_link = SerializerMethodField()
    children_link = SerializerMethodField()

    def get_body(self, obj):
        return obj.serve(request=self.context["request"]).render().content

    def get_parent(self, obj):
        parent = obj.get_parent()
        if parent and hasattr(parent, "cmspage"):
            return parent.cmspage.uuid

    def get_parent_link(self, obj):
        parent = obj.get_parent()
        if not parent or not hasattr(parent, "cmspage"):
            return ""
        return f'<Link to="/pages/{parent.cmspage.uuid}">{parent.cmspage.title}</Link>'

    def get_children_link(self, obj):
        data = []
        for page in obj.get_children():
            if hasattr(page, "cmspage"):
                data.append(f'<Link to="/pages/{page.cmspage.uuid}">{page.cmspage.title}</Link>')
        return data

    class Meta:
        model = CMSPage
        fields = [
            "uuid",
            "created_at",
            "title",
            "slug",
            "show_in_menus",
            "parent",
            "body",
            "parent_link",
            "children_link",
        ]


class PageListSerializer(BasePageSerializer):

    children = SerializerMethodField()

    def get_children(self, obj):
        qs = CMSPage.objects.live().filter(id__in=obj.get_children())
        return PageListSerializer(qs, many=True, context=self.context).data

    class Meta(BasePageSerializer.Meta):
        fields = BasePageSerializer.Meta.fields + [
            "children",
        ]


class PageDetailSerializer(BasePageSerializer):

    children = SerializerMethodField()

    def get_children(self, obj):
        return CMSPage.objects.live().filter(id__in=obj.get_children()).values_list("uuid")

    class Meta(BasePageSerializer.Meta):
        fields = BasePageSerializer.Meta.fields + [
            "children",
        ]


class PageWithVersionSerializer(serializers.Serializer):
    version = serializers.DateTimeField()
    data = PageListSerializer(many=True)
