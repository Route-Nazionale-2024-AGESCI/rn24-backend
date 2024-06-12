from rest_framework import serializers

from common.serializers import UUIDRelatedModelSerializer
from maps.models.location import Location


class LocationSerializer(UUIDRelatedModelSerializer):
    icon = serializers.CharField(source="annotated_icon")
    category = serializers.CharField(source="annotated_category")

    class Meta:
        model = Location
        fields = (
            "uuid",
            "created_at",
            "name",
            "coords",
            "polygon",
            "is_public",
            "category",
            "icon",
        )


class LocationWithVersionSerializer(serializers.Serializer):
    version = serializers.DateTimeField()
    data = LocationSerializer(many=True)
