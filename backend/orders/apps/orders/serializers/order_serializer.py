from rest_framework import serializers

from apps.orders.models import Order
from apps.orders.serializers.order_detail_serializer import OrderDetailSerializer



class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user_id','order_items', 'total_amount']
        read_only_fields = ['user_id','total_amount' ]