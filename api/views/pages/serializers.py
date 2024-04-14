from rest_framework.fields import SerializerMethodField

from cms.models.page import CMSPage
from common.serializers import UUIDRelatedModelSerializer


class BasePageSerializer(UUIDRelatedModelSerializer):

    body = SerializerMethodField()

    def get_body(self, obj):
        return obj.serve(request=self.context["request"]).render().content

    class Meta:
        model = CMSPage
        fields = [
            "uuid",
            "created_at",
            "title",
            "slug",
            "body",
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
