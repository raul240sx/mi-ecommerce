from rest_framework import serializers

from apps.orders.models import OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product_id', 'quantity']
        extra_kwargs = {
            'quantity': {'min_value':1},
        }