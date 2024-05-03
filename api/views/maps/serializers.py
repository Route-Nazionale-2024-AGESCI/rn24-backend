from rest_framework import serializers

from common.serializers import UUIDRelatedModelSerializer
from maps.models.location import Location


class LocationSerializer(UUIDRelatedModelSerializer):
    class Meta:
        model = Location
        fields = (
            "uuid",
            "created_at",
            "name",
            "coords",
            "polygon",
        )


class LocationWithVersionSerializer(serializers.Serializer):
    version = serializers.DateTimeField()
    data = LocationSerializer(many=True)
