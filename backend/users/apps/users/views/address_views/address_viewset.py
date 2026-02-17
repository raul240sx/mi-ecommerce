from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from apps.users.models.address import Address
from apps.users.serializers.address_serializers.address_serializer import AddressSerializer


class AddressViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        if not self.request.user or not self.request.user.is_authenticated:
            return Address.objects.none()
        return Address.objects.filter(user=self.request.user, is_active=True)
    
    def perform_destroy(self, instance):
        user = self.request.user

        with transaction.atomic():

            instance.soft_delete(actor=user)


    def destroy(self, request,*args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)

        return Response({'message':'Dirección eliminada correctamente'}, status=status.HTTP_200_OK)

        