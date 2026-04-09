from rest_framework import serializers

from apps.orders.models import Order
from apps.orders.serializers.order_detail_serializer import OrderDetailSerializer



class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user_id', 'user_address', 'order_items', 'total_amount', 'created_date', 'status']
        read_only_fields = ['id', 'user_id', 'user_address','total_amount', 'created_date', 'status']