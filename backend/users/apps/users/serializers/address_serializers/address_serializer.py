from django.db import transaction, IntegrityError

from rest_framework import serializers

from apps.users.models.address import Address


class AddressSerializer(serializers.ModelSerializer):
    commune_name = serializers.CharField(source='commune.name', read_only=True)
    region_name = serializers.CharField(source='commune.region.name', read_only=True)

    class Meta:
        model = Address
        fields = [
            'id',
            'street',
            'number',
            'apartment',
            'commune',
            'commune_name',
            'region_name',
            'is_main',
            'is_active'
        ]
        read_only_fields = ['is_active']

    

    def create(self, validated_data):

        user = self.context['request'].user
 
        with transaction.atomic():
            try:
                if validated_data.get('is_main', False):
                    Address.objects.select_for_update().filter(user=user, is_active=True, is_main=True).update(is_main=False)
                
                address = Address.objects.create(user=user, **validated_data)
                return address
            
            except IntegrityError:
                raise serializers.ValidationError({'message':'Conflicto de integridad al asignar dirección principal.'})



    def update(self, instance, validated_data):

        user = instance.user
        new_is_main = validated_data.get('is_main', instance.is_main)


        with transaction.atomic():
            try:
                if new_is_main and not instance.is_main:
                    Address.objects.select_for_update().filter(user=user, is_active=True, is_main=True).exclude(id=instance.id).update(is_main=False)

                instance = super().update(instance, validated_data)

            except IntegrityError:
                raise serializers.ValidationError({'message':'Conflicto de integridad al asignar dirección principal.'})
        return instance



