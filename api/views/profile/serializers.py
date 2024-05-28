from django.conf import settings
from rest_framework import serializers

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
            "location",
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
    is_staff = serializers.BooleanField(source="user.is_staff", read_only=True)
    public_key = serializers.SerializerMethodField()

    def get_public_key(self, obj):
        return settings.PUBLIC_KEY

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
            "is_staff",
            "public_key",
        )
