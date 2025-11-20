from rest_framework import serializers

from apps.users.models.address import Address



class AddressSerializer(serializers.ModelSerializer):
    # campos de lectura para obtener la info del nombre de la comuna y la region en base al id
    commune_name = serializers.CharField(source="commune.name", read_only=True)
    region_name = serializers.CharField(source="region.name", read_only=True)

    class Meta:
        model = Address
        fields = [
            'id',
            'street',
            'number',
            'apartment',
            'is_main',
            'commune',
            'commune_name',
            'region_name',
            'is_active',
        ]
        read_only_fields = ['is_active']

    def validate(self, attrs):
        """
        Seguridad:
        - Impedir que un usuario modifique direcciones de otro usuario.
        - Esto es crítico en producción.
        """
        request = self.context.get('request')

        if self.instance and self.instance.user != request.user:
            raise serializers.ValidationError('No puedes modificar esta dirección.')

        return attrs
    
    def create(self, validated_data):
        """
        - Asigna automáticamente el usuario autenticado.
        - Si se marca como principal, desmarca las demás.
        """
        user = self.context['request'].user

        if validated_data.get('is_main', False):
            Address.objects.filter(user=user, is_main=True).update(is_main=False)

        return Address.objects.create(user=user, **validated_data)


    def update(self, instance, validated_data):
        """
        - Maneja correctamente la reasignación de dirección principal.
        """
        user = self.context['request'].user

        if validated_data.get('is_main', False):
            Address.objects.filter(user=user, is_main=True).exclude(id=instance.id).update(is_main=False)

        return super().update(instance, validated_data)