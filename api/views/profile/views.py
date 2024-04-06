from rest_framework import generics

from api.views.profile.serializers import ProfileSerializer
from people.models.person import Person


class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get_object(self):
        return Person.objects.get(user=self.request.user)
