from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.models.address import Address
from apps.users.permissions.is_internal_service import IsInternalService


class VerifyAddressView(APIView):
    permission_classes = [IsInternalService]


    def get(self, request, *args, **kwargs):
        
        address_id = kwargs.get('address_id')
        user_id = request.query_params.get('user_id')

        if not address_id or not user_id:
            return Response({'detail': 'Address_id o user_id no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

        print(f'el tipo de address id es {type(address_id)} y el de user_id es {type(user_id)}')

        address = Address.objects.filter(id=address_id, user_id=int(user_id)).exists()

        print(f'Addres existe? {address}')

        return Response({'address': address}, status=status.HTTP_200_OK)
