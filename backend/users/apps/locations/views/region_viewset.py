from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.locations.models import Region
from apps.locations.serializers.region_serializer import RegionSerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filterset_fields = ['zone']

