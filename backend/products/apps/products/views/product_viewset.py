from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from apps.products.permissions.is_staff_permission import IsStaffPermission

from apps.products.serializers.product_serializer import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = self.get_serializer().Meta.model.objects.filter(state=True).select_related('category', 'measure_unit')
        return queryset

    def get_permissions(self):

        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]

        else:
            permission_classes = [IsStaffPermission]

        return [permission() for permission in permission_classes]
    


    def perform_create(self, serializer):
        serializer.save(user_id=getattr(self.request.user, 'id', None))


    def perform_update(self, serializer):
        serializer.save(user_id=getattr(self.request.user, 'id', None))


    def perform_destroy(self, instance):
        instance.delete(user_id=getattr(self.request.user, 'id', None))


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        return Response({'message':'Producto deshabilitado correctamente'}, status=status.HTTP_200_OK)

