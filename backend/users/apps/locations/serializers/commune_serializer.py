from rest_framework import serializers

from apps.locations.models import Commune
from apps.locations.serializers.region_serializer import RegionSerializer


class CommuneSerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = Commune
        fields = [
            'id',
            'name',
            'region',
        ]