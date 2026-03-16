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
            'password':{
                'write_only':True,
                'error_messages': {
                'blank': ['El campo Contraseña no puede estar vacío.'],
                'required': ['Este campo es obligatorio.'],
                }
            },
            'email': {
                'validators': [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message=['Ya existe un usuario registrado con este email']
                    )
                ],
                'error_messages':{
                    'invalid': ['Por favor, introduce una dirección de correo válida.'],
                    'blank':['El correo electrónico no puede estar vacío.']
                }
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
            raise serializers.ValidationError([
                    'Mínimo 8 caracteres',
                    'No ser similar a tu email',
                    'No ser una contraseña muy común',
                    'No ser exclusivamente numérica'
                    ]
                )
        
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
    



