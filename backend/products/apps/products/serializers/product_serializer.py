from rest_framework import serializers

from apps.products.models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'category',
            'measure_unit',
            'image',
            'stock',
        ]
        read_only_fields = ['id']


    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['category'] = {
            'id': instance.category.id,
            'name': instance.category.name
            } if instance.category and instance.category.state else None
        
        data['measure_unit'] = {
            'id': instance.measure_unit.id,
            'name': instance.measure_unit.name
            } if instance.measure_unit and instance.measure_unit.state else None

        return data
