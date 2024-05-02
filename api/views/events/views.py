from rest_framework import generics

from api.views.events.serializers import (
    EventInvitationSerializer,
    EventRegistrationSerializer,
    EventSerializer,
)
from events.models.event import Event
from events.models.event_registration import PersonEventRegistration
from events.services.registration import delete_personal_registration
from events.services.selectors import get_events_registered_to_person, get_events_visible_to_person


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.order_by("starts_at").all()


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
