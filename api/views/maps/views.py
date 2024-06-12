from django.db.models import F
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics

from api.views.maps.serializers import LocationSerializer, LocationWithVersionSerializer
from maps.models.location import Location


def get_location_queryset():
    return (
        Location.objects.select_related("category")
        .annotate(
            annotated_icon=F("category__icon"),
            annotated_category=F("category__name"),
        )
        .all()
    )


@extend_schema_view(get=extend_schema(operation_id="api_v1_locations_list"))
class LocationListView(generics.RetrieveAPIView):
    serializer_class = LocationWithVersionSerializer

    def get_object(self):
        return {
            "version": Location.get_last_updated_timestamp(),
            "data": get_location_queryset(),
        }


class LocationDetailView(generics.RetrieveAPIView):
    serializer_class = LocationSerializer
    queryset = get_location_queryset()
    lookup_field = "uuid"
    lookup_url_kwarg = "uuid"
