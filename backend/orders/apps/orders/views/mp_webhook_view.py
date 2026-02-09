import mercadopago

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.orders.services.mercadopago_service import MercadoPagoService
from apps.orders.models.order import Order



@method_decorator(csrf_exempt, name='dispatch')
class MpWebhookView(APIView):
    permission_classes = [AllowAny]


    def post(self,request):
        payment_id = request.data.get('data',{}).get('id')
        payment_type = request.data.get('type')


        if not payment_id:
            return Response({'detail':'No se ha encontrado el id de pago'}, status=status.HTTP_400_BAD_REQUEST)
        
        if payment_type != 'payment':
            return Response({'detail':'Tipo de pago no válido, petición ignorada'}, status=status.HTTP_200_OK)
        

        mp = MercadoPagoService()

        mp_response = mp.get_payment_info(payment_id)

        mp_detail = mp_response.get('response')

        if mp_response.get('status') != 200:
            return Response({'detail': f'Error al intentar comprobar el pago de la orden id: {payment_id}'}, status=status.HTTP_400_BAD_REQUEST)
        
        if mp_detail.get('status') == 'approved':
            order_id = mp_detail.get('external_reference')


            if not order_id:
                return Response({'detail': f'No se encuentra la referencia a la orden original del id de pago: {payment_id}'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                order_id = int(order_id)
            except ValueError:
                return Response({'detail': f'Tipo de dato de referencia a la orden original iválido. Id de pago: {payment_id}'}, status=status.HTTP_400_BAD_REQUEST)
            
            
            order = Order.objects.filter(id=order_id, state=True).first()

            if not order:
                return Response({'detail': f'No se encuentra la orden {order_id} en la base de datos'}, status=status.HTTP_400_BAD_REQUEST)
                                 
            if order.status != Order.Status.PENDING:
                return Response({'detail':'Pago no válido debido a que la orden ya está pagada o cancelada'}, status=status.HTTP_400_BAD_REQUEST)

            order.status = Order.Status.PAID
            order.save(update_fields=['status'])

            return Response({'message':'Producto pagado correctamente'}, status=status.HTTP_200_OK)
        
        return Response({'detail':'Status de pago no válido'}, status=status.HTTP_200_OK)
        
