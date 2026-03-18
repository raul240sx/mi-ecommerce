from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from apps.orders.models.order import Order
from apps.orders.services.mercadopago_service import MercadoPagoService
from apps.base.exceptions import PaymentError




mp = MercadoPagoService()


class MpPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.user.id

        order_id = kwargs.get('id')
        order = Order.objects.filter(id=order_id, state=True).first()

        if (user_id != str(order.user_id)) or (not order) or (order.status != Order.Status.PENDING):
            return Response({'message':'Solicitud de pago no válida'}, status=status.HTTP_400_BAD_REQUEST)

        
        payment_init_point = None
        mp_error = False

        try:
            payment_preference = mp.create_payment_preference(order)
            payment_init_point = payment_preference.get('init_point')

        except PaymentError as e:
            raise ValidationError({'detail':str(e)})
        
        except Exception as e:
            mp_error = True


        response_data = {
            'message':'Orden creada correctamente',
            'Order ID':order_id,
            'payment_link':payment_init_point
            }

        if mp_error:
            response_data['message'] = 'Ordern creada, pero hubo un problema con el proveedor al generar el link de pago'
            response_data['note'] = 'Puede volver a intentar generar el link de pago desde tu historial de pedidos'

        return Response(response_data, status=status.HTTP_201_CREATED)



