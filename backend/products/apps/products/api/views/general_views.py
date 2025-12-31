from rest_framework import viewsets

from apps.base.api import GeneralListApiView
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, IndicatorSerializer, CategoryProductSerializer


class MeasureUnitViewSet(viewsets.ModelViewSet):
    serializer_class = MeasureUnitSerializer
    queryset = MeasureUnitSerializer.Meta.model.objects.filter(state=True)
    
    
class IndicatorViewSet(viewsets.ModelViewSet):
    serializer_class = IndicatorSerializer
    queryset = MeasureUnitSerializer.Meta.model.objects.filter(state=True)


class CategoryProductViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryProductSerializer
    queryset = MeasureUnitSerializer.Meta.model.objects.filter(state=True)



