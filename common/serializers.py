from rest_framework.serializers import ModelSerializer, SlugRelatedField


class UUIDRelatedField(SlugRelatedField):
    def __init__(self, slug_field=None, **kwargs):
        super().__init__(slug_field="uuid", **kwargs)


class UUIDRelatedModelSerializer(ModelSerializer):
    serializer_related_field = UUIDRelatedField
