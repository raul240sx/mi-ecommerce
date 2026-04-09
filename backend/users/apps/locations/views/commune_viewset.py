from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.locations.models import Commune
from apps.locations.serializers.commune_serializer import CommuneSerializer


class CommuneViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    queryset = Commune.objects.all()
    serializer_class = CommuneSerializer
    filterset_fields = ['region']

