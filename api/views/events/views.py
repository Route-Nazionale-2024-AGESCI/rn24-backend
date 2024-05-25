from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics

from api.views.events.serializers import (
    EventInvitationSerializer,
    EventRegistrationSerializer,
    EventSerializer,
    EventWithVersionSerializer,
)
from events.models.event import Event
from events.models.event_registration import PersonEventRegistration
from events.services.registration import delete_personal_registration
from events.services.selectors import get_events_registered_to_person, get_events_visible_to_person


@extend_schema_view(get=extend_schema(operation_id="api_v1_events_list"))
class EventListView(generics.RetrieveAPIView):
    serializer_class = EventWithVersionSerializer

    def get_object(self):
        return {
            "version": Event.get_last_updated_timestamp(),
            "data": Event.objects.select_related("location", "page").order_by("starts_at").all(),
        }


class EventDetailView(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class EventRegistrationListView(generics.ListCreateAPIView):
    serializer_class = EventRegistrationSerializer

    def get_queryset(self):
        return get_events_registered_to_person(self.request.user.person)


class EventRegistrationDetailView(generics.DestroyAPIView):
    serializer_class = EventRegistrationSerializer

    def get_queryset(self):
        return PersonEventRegistration.objects.filter(person=self.request.user.person)

    def get_object(self):
        return self.get_queryset().get(event__uuid=self.kwargs["uuid"])

    def perform_destroy(self, instance):
        delete_personal_registration(self.request.user.person, instance.event)


class EventInvitationListView(generics.ListAPIView):
    serializer_class = EventInvitationSerializer

    def get_queryset(self):
        return get_events_visible_to_person(self.request.user.person)
