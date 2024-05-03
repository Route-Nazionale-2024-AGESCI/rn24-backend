from rest_framework import serializers


class VersionSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.URLField()
    version = serializers.DateTimeField()
