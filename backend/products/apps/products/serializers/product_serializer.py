from rest_framework import serializers

from apps.products.models.product_model import Product


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'price',
            'category',
            'measure_unit',
            'image'
        ]


    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['category'] = {
            'id': instance.category.id,
            'name': instance.category.name
            } if instance.category else None
        
        data['measure_unit'] = {
            'id': instance.measure_unit.id,
            'name': instance.measure_unit.name
            } if instance.measure_unit else None

        return data
