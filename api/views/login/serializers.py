from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from authentication.AGESCI import AGESCIResetPasswordClient


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
        return {
            "token": request.user.auth_token.key,
            "csrftoken": request.META["CSRF_COOKIE"],
        }


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    agesci_id = serializers.CharField(write_only=True)
    message = serializers.CharField(read_only=True)

    def create(self, validated_data):
        success, message = AGESCIResetPasswordClient().send_reset_password_email(
            agesci_id=validated_data["agesci_id"], email=validated_data["email"]
        )
        if not success:
            raise ValidationError({"message": message})
        return {"message": message}

    def to_representation(self, instance):
        return instance
