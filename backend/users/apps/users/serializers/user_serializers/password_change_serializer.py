import re
from rest_framework import serializers



class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_new_password = serializers.CharField(required=True, write_only=True)


    def  validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'old_password':'Contraseña actual incorrecta'})
        return value
    

    def validate_new_password(self, value):
        # Verificar longitud del string
        if len(value) < 8:
            raise serializers.ValidationError({'new_password':'La contraseña debe tener al menos 8 caracteres'})

        # Verificar con una expresion regular si cumple con al menos una mayuscula una minuscula y un numero.
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).+$'

        if not bool(re.fullmatch(pattern, value)):
            raise serializers.ValidationError({'new_password':'La contraseña debe tener al menos una mayúscula, una minuscula y un número'})

        return value
    
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({'confirm_new_password':'Las contraseñas no coinciden'})
        
        return attrs
    
    
    def save(self):
        user = self.context['request'].user
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()

        return user
    

        