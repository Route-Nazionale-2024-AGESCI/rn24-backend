from django.urls import path
from django.views.decorators.cache import cache_page
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api.views.badges.views import BadgeDetailPDFView, BadgeDetailView
from api.views.events.views import (
    EventAttendeesListView,
    EventCheckInDetailView,
    EventDetailView,
    EventInvitationListView,
    EventListView,
    EventQRDetailView,
    EventRegistrationDetailView,
    EventRegistrationListView,
)
from api.views.login.views import LoginView, LogoutView, PasswordGenerateView, PasswordResetView
from api.views.maps.views import LocationDetailView, LocationListView
from api.views.pages.views import PageDetailView, PageListView, PageQRDetailView
from api.views.profile.views import ProfileDetailView
from api.views.version.views import VersionListView
from rn24.settings import CACHE_TIMEOUT

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
    path("auth/password-generate/", PasswordGenerateView.as_view(), name="password-generate"),
    path("badges/<uuid:uuid>.html", BadgeDetailView.as_view(), name="badge-detail"),
    path("badges/<uuid:uuid>.pdf", BadgeDetailPDFView.as_view(), name="badge-detail-pdf"),
    path("profile/", ProfileDetailView.as_view(), name="profile-detail"),
    path("versions/", VersionListView.as_view(), name="version-list"),
    path("locations/", cache_page(CACHE_TIMEOUT)(LocationListView.as_view()), name="location-list"),
    path("locations/<uuid:uuid>/", LocationDetailView.as_view(), name="location-detail"),
    path("events/", cache_page(CACHE_TIMEOUT)(EventListView.as_view()), name="event-list"),
    path("events/<uuid:uuid>/", EventDetailView.as_view(), name="event-detail"),
    path(
        "events/<uuid:uuid>/check-in/",
        EventCheckInDetailView.as_view(),
        name="event-check-in-detail",
    ),
    path("events/<uuid:uuid>/qr/", EventQRDetailView.as_view(), name="event-qr-detail"),
    path(
        "events/<uuid:uuid>/attendees/",
        EventAttendeesListView.as_view(),
        name="event-attendees-list",
    ),
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
    path("pages/", cache_page(CACHE_TIMEOUT)(PageListView.as_view()), name="page-list"),
    path("pages/<uuid:uuid>/", PageDetailView.as_view(), name="page-detail"),
    path("pages/<uuid:uuid>/qr/", PageQRDetailView.as_view(), name="page-qr-detail"),
]
