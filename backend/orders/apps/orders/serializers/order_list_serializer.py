from rest_framework import serializers

from apps.orders.models.order import Order

class OrderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_amount', 'created_date', 'modified_date']
        read_only_fields = fields