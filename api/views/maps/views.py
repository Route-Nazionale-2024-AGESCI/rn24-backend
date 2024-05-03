from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics

from api.views.maps.serializers import LocationSerializer, LocationWithVersionSerializer
from maps.models.location import Location


@extend_schema_view(get=extend_schema(operation_id="api_v1_locations_list"))
class LocationListView(generics.RetrieveAPIView):
    serializer_class = LocationWithVersionSerializer

    def get_object(self):
        return {
            "version": Location.get_last_updated_timestamp(),
            "data": Location.objects.all(),
        }


class LocationDetailView(generics.RetrieveAPIView):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
