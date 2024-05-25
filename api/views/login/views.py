from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework import generics

from api.views.login.serializers import LoginSerializer, PasswordResetSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []


class LogoutView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class PasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetSerializer
    authentication_classes = []
    permission_classes = []
    queryset = []
