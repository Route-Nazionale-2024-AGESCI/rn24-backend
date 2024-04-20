from common.serializers import UUIDRelatedModelSerializer
from people.models.district import District
from people.models.person import Person
from people.models.scout_group import ScoutGroup
from people.models.squad import Squad
from people.models.subdistrict import Subdistrict


class SquadSerializer(UUIDRelatedModelSerializer):
    class Meta:
        model = Squad
        fields = (
            "uuid",
            "name",
        )


class DistrictSerializer(UUIDRelatedModelSerializer):
    class Meta:
        model = District
        fields = (
            "uuid",
            "name",
        )


class SubdistrictSerializer(UUIDRelatedModelSerializer):
    district = DistrictSerializer()

    class Meta:
        model = Subdistrict
        fields = (
            "uuid",
            "name",
            "district",
        )


class ScoutGroupSerializer(UUIDRelatedModelSerializer):
    subdistrict = SubdistrictSerializer()

    class Meta:
        model = ScoutGroup
        fields = (
            "uuid",
            "name",
            "zone",
            "region",
            "subdistrict",
            "happiness_path",
        )


class ProfileSerializer(UUIDRelatedModelSerializer):
    scout_group = ScoutGroupSerializer()
    squads = SquadSerializer(many=True)

    class Meta:
        model = Person
        fields = (
            "uuid",
            "agesci_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "scout_group",
            "squads",
        )
