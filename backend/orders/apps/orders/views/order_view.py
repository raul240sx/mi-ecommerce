from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.serializers.order_serializer import OrderSerializer


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        request_user = request.user.id

        order_id = kwargs.get('id')
        order = OrderSerializer.Meta.model.objects.filter(id=order_id, state=True).prefetch_related('order_items').first()

        if order and request_user == order.user_id:
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'detail':'Orden no encontrada'}, status=status.HTTP_404_NOT_FOUND)

