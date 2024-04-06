from rest_framework import generics

from api.views.locations.serializers import LocationSerializer
from maps.models.location import Location


class LocationListView(generics.ListAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()


class LocationDetailView(generics.RetrieveAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
