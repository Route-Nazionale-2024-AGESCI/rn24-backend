from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api.views.badges.views import BadgeDetailView
from api.views.events.views import (
    EventDetailView,
    EventInvitationListView,
    EventListView,
    EventRegistrationDetailView,
    EventRegistrationListView,
)
from api.views.login.views import LoginView, LogoutView, PasswordResetView
from api.views.maps.views import LocationDetailView, LocationListView
from api.views.pages.views import PageDetailView, PageListView
from api.views.profile.views import ProfileDetailView
from api.views.version.views import VersionListView

urlpatterns = [
    # path("api-auth/", include("rest_framework.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path("badges/<uuid:uuid>/", BadgeDetailView.as_view(), name="badge-detail"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail"),
    path("versions/", VersionListView.as_view(), name="version-list"),
    path("locations/", LocationListView.as_view(), name="location-list"),
    path("locations/<uuid:uuid>/", LocationDetailView.as_view(), name="location-detail"),
    path("events/", EventListView.as_view(), name="event-list"),
    path("events/<uuid:uuid>/", EventDetailView.as_view(), name="event-detail"),
    path(
        "events/registrations/",
        EventRegistrationListView.as_view(),
        name="event-registration-list",
    ),
    path(
        "events/registrations/<uuid:uuid>/",
        EventRegistrationDetailView.as_view(),
        name="event-registration-detail",
    ),
    path("events/invitations/", EventInvitationListView.as_view(), name="event-invitation-list"),
    path("pages/", PageListView.as_view(), name="page-list"),
    path("pages/<uuid:uuid>/", PageDetailView.as_view(), name="page-detail"),
]
