from rest_framework import generics

from api.views.events.serializers import EventSerializer
from events.models.event import Event


class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventDetailView(generics.RetrieveAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
