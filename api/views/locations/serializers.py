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
