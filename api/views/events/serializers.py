from rest_framework import serializers

from common.serializers import UUIDRelatedModelSerializer
from events.models.event import Event


class EventSerializer(UUIDRelatedModelSerializer):
    class Meta:
        model = Event
        fields = (
            "uuid",
            "created_at",
            "name",
            "location",
            "is_registration_required",
            "registration_limit",
            "registration_limit_from_same_scout_group",
            "starts_at",
            "ends_at",
            "registrations_open_at",
            "registrations_close_at",
            "kind",
        )


class EventRegistrationSerializer(serializers.Serializer):
    event = serializers.UUIDField(source="uuid")
    is_personal = serializers.BooleanField()


class EventInvitationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
