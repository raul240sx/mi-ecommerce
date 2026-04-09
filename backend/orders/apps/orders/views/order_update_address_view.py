import requests

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from apps.orders.models.order import Order
from apps.orders.serializers.order_serializer import OrderSerializer



class OrderUpdateAddressView(APIView):
    permission_classes = [IsAuthenticated]


    def patch(self, request, *args, **kwargs):
        headers = {'Internal-Service-Key': settings.INTERNAL_SERVICE_KEY}

        order_id_str = request.data.get('orderId')
        address_id_str = request.data.get('addressId')

        if not order_id_str or not address_id_str:
            return Response({'detail': 'orderId y addressId son requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order_id = int(order_id_str)
            address_id = int(address_id_str)
            
        except Exception:
            return Response({'detail': 'Numero de orden o de dirección mal formateados'}, status=status.HTTP_400_BAD_REQUEST)


        order = Order.objects.filter(id=order_id).first()

        if not order:
            return Response({'detail': 'No es posible obtener los datos de la orden'}, status=status.HTTP_400_BAD_REQUEST)
        
        if order.user_id != int(request.user.id):
            return Response({'detail': 'Orden no disponible'}, status=status.HTTP_400_BAD_REQUEST)
        
        response = requests.get(f'http://users-service:8000/users-api/verify-address/{address_id}/?user_id={int(request.user.id)}', headers=headers, timeout=5)

        if response.status_code == 200:
            address_found = response.json().get('address')

            print(f'en orders, la respuest la respuesta de users es: {address_found}')

            if address_found:
                order.user_address = address_id
                order.save()

                return Response({'detail': 'Dirección actualizada correctamente', 'orden': OrderSerializer(order).data}, status=status.HTTP_200_OK)
           

        return Response({'detail': 'Error al verificar la dirección'}, status=status.HTTP_400_BAD_REQUEST)

        

        

