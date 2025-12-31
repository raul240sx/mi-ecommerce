import re
from rest_framework import serializers

from apps.users.models.user import User


class UserUpdateSerializer(serializers.ModelSerializer):
    allowed_write_fields = ['first_name', 'last_name', 'phone']


    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
        ]
        


    def validate(self, attrs):
        phone = attrs.get('phone')
        if phone:
            if len(phone) != 9 or not phone.isdigit():
                raise serializers.ValidationError({'phone': 'Número de teléfono inválido (9 dígitos numéricos)'})

        name_pattern = r"^[A-Za-zÁÉÍÓÚÜáéíóúüÑñ]+(?:[ '\-][A-Za-zÁÉÍÓÚÜáéíóúüÑñ]+)*$"

        for field in ['first_name', 'last_name']:
            value = attrs.get(field)
            if value:
                value_stripped = value.strip()
                if len(value_stripped) < 2 or not re.fullmatch(name_pattern, value_stripped):
                    raise serializers.ValidationError({field: f'{field} no válido'})
                attrs[field] = value_stripped  

        return attrs
    

    
    def update(self, instance, validated_data):

        for field in ['first_name', 'last_name', 'phone']:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.save()


        return instance
        