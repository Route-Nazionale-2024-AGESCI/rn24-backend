from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        username = attrs.get("username", None)
        password = attrs.get("password", None)
        user = authenticate(username=username, password=password)

        if user is None:
            raise AuthenticationFailed()
        else:
            request = self.context.get("request")
            login(request, user)
            return attrs

    def create(self, validated_data):
        return True

    def to_representation(self, instance):
        request = self.context.get("request")
        return {"token": request.user.auth_token.key}
