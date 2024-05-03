from django.urls import reverse
from rest_framework import generics

from api.views.version.serializers import VersionSerializer
from cms.models.page import CMSPage
from events.models.event import Event
from maps.models.location import Location


class VersionListView(generics.ListAPIView):
    serializer_class = VersionSerializer

    def get_queryset(self):
        return [
            {
                "name": "pages",
                "url": reverse("page-list"),
                "version": CMSPage.get_last_updated_timestamp(),
            },
            {
                "name": "events",
                "url": reverse("event-list"),
                "version": Event.get_last_updated_timestamp(),
            },
            {
                "name": "locations",
                "url": reverse("location-list"),
                "version": Location.get_last_updated_timestamp(),
            },
        ]
