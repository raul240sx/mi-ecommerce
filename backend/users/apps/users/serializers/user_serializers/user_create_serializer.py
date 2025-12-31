from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import BaseUserManager
from django.core import exceptions as django_exceptions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.users.models.user import User


class UserCreateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'confirm_password'
        ]
        read_only_fields = ['id']

        extra_kwargs = {
            'password':{'write_only':True},
            'email': {
                'validators': [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message='Ya existe un usuario registrado con este email'
                    )
                ]
            }
        }



    def validate_email(self, value):
        value = value.strip().lower()
        value = BaseUserManager.normalize_email(value)
        
        return value

    
    def validate_password(self, value):
        try:
            validate_password(value)
        except django_exceptions.ValidationError:
            raise serializers.ValidationError('Contraseña no válida. La contraseña debe cumplir:\n'
            '1. Mínimo 8 caracteres.\n'
            '2. No ser similar a tu email.\n'
            '3. No ser una contraseña muy común.\n'
            '4. No ser exclusivamente numérica.')
        
        return value


    def validate(self, attrs):

        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'confirm_password': 'Las contraseñas no coinciden.'})
        
        return attrs


    def create(self, validated_data):
        # Borrar contraseña del diccionario
        password = validated_data.pop('password')
        validated_data.pop('confirm_password', None) 

        user = User.objects.create_user(password=password, **validated_data)

        return user
    



