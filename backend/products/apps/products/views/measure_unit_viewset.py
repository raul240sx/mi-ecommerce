from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.products.serializers.measure_unit_serializer import MeasureUnitSerializer
from apps.products.permissions.is_staff_permission import IsStaffPermission


class MeasureUnitViewSet(ModelViewSet):
    serializer_class = MeasureUnitSerializer
    permission_classes = [IsStaffPermission]

    def get_queryset(self):
        queryset = self.get_serializer().Meta.model.objects.filter(state=True)
        return queryset
    

    def perform_create(self, serializer):
        serializer.save(user_id=getattr(self.request.user, 'id', None))

    def perform_update(self, serializer):
        serializer.save(user_id=getattr(self.request.user, 'id', None))

    def perform_destroy(self, instance):
        instance.delete(user_id=getattr(self.request.user, 'id', None))

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)

        return Response({'message':'Unidad de medida deshabilitada correctamente'}, status=status.HTTP_200_OK)
