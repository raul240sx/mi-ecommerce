from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from apps.orders.services import validate_and_get_products_info
from apps.orders.serializers.order_serializer import OrderSerializer
from apps.orders.services.mercadopago_service import MercadoPagoService
from apps.base.exceptions import PaymentError




mp = MercadoPagoService()



class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_init_point = None
        mp_error = False
        try:
            order = validate_and_get_products_info(serializer.validated_data['order_items'], user_id)

            try:
                payment_preference = mp.create_payment_preference(order)
                payment_init_point = payment_preference.get('init_point')

            except PaymentError as e:
                raise ValidationError({'detail':str(e)})
            
            except Exception as e:
                mp_error = True

            serializer = OrderSerializer(order)

            response_data = {
                'message':'Orden creada correctamente',
                'Order':serializer.data,
                'payment_link':payment_init_point
                }

            if mp_error:
                response_data['message'] = 'Ordern creada, pero hubo un problema con el proveedor al generar el link de pago'
                response_data['note'] = 'Puede volver a intentar generar el liink de pago desde tu historial de pedidos'

            return Response(response_data, status=status.HTTP_201_CREATED)


        except ValidationError as e:
            return Response({'detail':str(e)}, status=status.HTTP_400_BAD_REQUEST)

