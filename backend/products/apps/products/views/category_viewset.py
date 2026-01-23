from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from apps.products.serializers.category_serializer import CategorySerializer
from apps.products.permissions.is_staff_permission import IsStaffPermission



class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = self.get_serializer().Meta.model.objects.filter(state=True)
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
        super().destroy(request, *args, **kwargs)

        return Response({'message':'Categoría deshabilitada correctamente'}, status=status.HTTP_200_OK)

