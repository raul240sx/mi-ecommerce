from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from drf_yasg.utils import swagger_auto_schema

from apps.products.permissions.is_staff_permission import IsStaffPermission

from apps.products.serializers.product_serializer import ProductSerializer



@method_decorator(name='list', decorator=swagger_auto_schema(security=[]))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(security=[]))
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = self.get_serializer().Meta.model.objects.filter(state=True).select_related('category', 'measure_unit')
        return queryset
    

    def get_authenticators(self):
        action = getattr(self, 'action', None)
        if action in ['list', 'retrieve', 'None']:
            return []
        
        return [auth() for auth in self.authentication_classes]


    def get_permissions(self):
        action = getattr(self, 'action', None)
        if action in ['list', 'retrieve', 'None']:
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

