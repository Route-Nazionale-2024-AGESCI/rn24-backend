from rest_framework import generics

from api.views.login.serializers import LoginSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []
