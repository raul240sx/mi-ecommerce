from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from apps.orders.services import validate_and_get_products_info
from apps.orders.serializers.order_serializer import OrderSerializer



class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id

        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            order = validate_and_get_products_info(serializer.validated_data['order_items'], user_id)

            serializer = OrderSerializer(order)

            response_data = {
                'message':'Orden creada correctamente',
                'Order':serializer.data,
                }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'detail':str(e)}, status=status.HTTP_400_BAD_REQUEST)

