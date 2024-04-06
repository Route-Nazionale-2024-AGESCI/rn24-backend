from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api.views.events.views import EventDetailView, EventListView
from api.views.locations.views import LocationDetailView, LocationListView
from api.views.profile.views import ProfileDetailView

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail"),
    path("locations/", LocationListView.as_view(), name="location-list"),
    path("locations/<uuid:uuid>/", LocationDetailView.as_view(), name="location-detail"),
    path("events/", EventListView.as_view(), name="event-list"),
    path("events/<uuid:uuid>/", EventDetailView.as_view(), name="event-detail"),
]
