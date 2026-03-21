from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.orders.serializers.order_list_serializer import OrderListSerializer


class OrderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer

    def get_queryset(self):
        print('llegué al get queryset')
        print()
        return self.get_serializer().Meta.model.objects.filter(state=True, user_id=self.request.user.id)
    