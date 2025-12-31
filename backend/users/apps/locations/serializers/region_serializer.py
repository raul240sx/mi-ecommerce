from rest_framework import serializers

from apps.locations.models import Region


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = [
            'id',
            'name',
            'zone',
        ]

