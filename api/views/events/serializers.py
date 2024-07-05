from django.shortcuts import get_object_or_404
from rest_framework import serializers

from common.serializers import UUIDRelatedModelSerializer
from events.models.event import Event
from events.services.registration import register_person_to_event


class EventSerializer(UUIDRelatedModelSerializer):
    class Meta:
        model = Event
        fields = (
            "uuid",
            "created_at",
            "id",
            "name",
            "page",
            "location",
            "is_registration_required",
            "registration_limit",
            "registration_limit_from_same_scout_group",
            "personal_registrations_count",
            "starts_at",
            "ends_at",
            "registrations_open_at",
            "registrations_close_at",
            "kind",
            "correlation_id",
            "happiness_path",
        )


class EventRegistrationSerializer(serializers.Serializer):
    event = serializers.UUIDField(source="uuid")
    is_personal = serializers.BooleanField(read_only=True)

    def validate_event(self, value):
        event = get_object_or_404(Event, uuid=value)
        return event

    def create(self, validated_data):
        event = validated_data["uuid"]
        person = self.context["request"].user.person
        register_person_to_event(person, event)
        return event


class EventInvitationSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()


class EventWithVersionSerializer(serializers.Serializer):
    version = serializers.DateTimeField()
    data = EventSerializer(many=True)


class EventCheckinDetailSerializer(serializers.Serializer):
    check_in = serializers.BooleanField(read_only=True)
