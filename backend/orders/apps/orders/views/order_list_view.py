from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from apps.orders.serializers.order_list_serializer import OrderListSerializer


class OrderListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer


    filter_backends = [DjangoFilterBackend, filters.OrderingFilter ]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'total_amount']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state=True, user_id=self.request.user.id)
    
