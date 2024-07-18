from django.conf import settings
from rest_framework import serializers

from common.serializers import UUIDRelatedModelSerializer
from people.models.district import District
from people.models.line import Line
from people.models.person import Person
from people.models.scout_group import ScoutGroup
from people.models.squad import Squad
from people.models.subdistrict import Subdistrict


class SquadSerializer(UUIDRelatedModelSerializer):
    class Meta:
        model = Squad
        fields = ("uuid", "name", "page")


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


class LineSerializer(UUIDRelatedModelSerializer):
    subdistrict = SubdistrictSerializer()

    class Meta:
        model = Line
        fields = (
            "uuid",
            "name",
            "subdistrict",
            "location",
        )


class ScoutGroupSerializer(UUIDRelatedModelSerializer):
    line = LineSerializer()

    class Meta:
        model = ScoutGroup
        fields = (
            "uuid",
            "name",
            "zone",
            "region",
            "line",
            "happiness_path",
        )


class PermissionsSerializer(serializers.Serializer):
    is_staff = serializers.BooleanField(source="user.is_staff", read_only=True)
    can_scan_qr = serializers.BooleanField(read_only=True)


class PersonalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "identity_document_type",
            "identity_document_number",
            "identity_document_issue_date",
            "identity_document_expiry_date",
            "accessibility_has_wheelchair",
            "accessibility_has_caretaker_not_registered",
            "sleeping_is_sleeping_in_tent",
            "sleeping_requests",
            "sleeping_place",
            "sleeping_requests_2",
            "food_diet_needed",
            "food_allergies",
            "food_is_vegan",
            "transportation_has_problems_moving_on_foot",
            "transportation_need_transport",
            "health_has_allergies",
            "health_allergies",
            "health_has_movement_disorders",
            "health_movement_disorders",
            "health_has_patologies",
            "health_patologies",
        )


class ProfileSerializer(UUIDRelatedModelSerializer):
    scout_group = ScoutGroupSerializer()
    squads = SquadSerializer(many=True)
    public_key = serializers.SerializerMethodField()
    qr_code = serializers.SerializerMethodField()
    permissions = PermissionsSerializer(source="*")
    personal_data = PersonalDataSerializer(source="*")

    def get_public_key(self, obj):
        return settings.PUBLIC_KEY

    def get_qr_code(self, obj):
        return obj.qr_string_with_signature()

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
            "public_key",
            "qr_code",
            "permissions",
            "personal_data",
        )


class PersonSummarySerializer(UUIDRelatedModelSerializer):
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
