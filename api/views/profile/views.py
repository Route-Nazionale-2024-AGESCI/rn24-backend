import logging

from django.http import Http404
from rest_framework import generics

from api.views.profile.serializers import ProfileSerializer
from people.models.person import Person

logger = logging.getLogger(__name__)


class ProfileDetailView(generics.RetrieveAPIView, generics.UpdateAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        try:
            return Person.objects.get(user=self.request.user)
        except Person.DoesNotExist:
            logger.error(f"Person with user {self.request.user} not found")
            raise Http404
