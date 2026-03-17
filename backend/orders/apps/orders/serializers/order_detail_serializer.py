from rest_framework import serializers

from apps.orders.models import OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['product_id', 'product_title', 'quantity', 'unit_price', 'image_url']
        read_only_fields = ['product_title', 'unit_price', 'image_url']
        extra_kwargs = {
            'quantity': {'min_value':1},
        }