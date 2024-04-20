from rest_framework import generics

from api.views.events.serializers import (
    EventInvitationSerializer,
    EventRegistrationSerializer,
    EventSerializer,
)
from events.models.event import Event
from events.services.selectors import get_events_registered_to_person, get_events_visible_to_person


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventDetailView(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"


class EventRegistrationListView(generics.ListAPIView):
    serializer_class = EventRegistrationSerializer

    def get_queryset(self):
        return get_events_registered_to_person(self.request.user.person)


class EventInvitationListView(generics.ListAPIView):
    serializer_class = EventInvitationSerializer

    def get_queryset(self):
        return get_events_visible_to_person(self.request.user.person)