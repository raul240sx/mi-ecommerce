from rest_framework import serializers

from apps.products.models.measure_unit import MeasureUnit


class MeasureUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasureUnit
        fields = [
            'id',
            'name'
        ]

