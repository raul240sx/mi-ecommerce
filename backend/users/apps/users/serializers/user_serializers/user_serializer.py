from rest_framework import serializers

from apps.users.models.user import User


## SERIALIZADOR PARA MOSTRAR DATOS DEL USUARIO EN UNA SECCION "MI PERFIL"

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_joined',
            'is_verified',
            'is_profile_complete',
        ]
