from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework import serializers

from apps.users.models.user import User


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)


    def validate_new_password(self, value):
        validate_password(value)
        return value
    

    def validate(self, attrs):
        # validacion concordancia de contraseñas
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({'confirm_new_password':'Las contraseñas no coinciden'})

        
        try:
            #decodificar uid
            uid_decoded = smart_str(urlsafe_base64_decode(attrs['uidb64']))

            #obtener usuario
            user = User.objects.get(id=uid_decoded)


        except (TypeError, ValueError, OverflowError, DjangoUnicodeDecodeError, User.DoesNotExist):
            raise serializers.ValidationError({'detail':'El enlace de restablecimiento es inválido o ha expirado.'})
        

        token_ok = PasswordResetTokenGenerator().check_token(user, attrs.get('token'))
        if not token_ok:
            # 🔑 Nota: Si el token falla, es el mismo error de seguridad.
            raise serializers.ValidationError({'detail':'El enlace de restablecimiento es inválido o ha expirado.'})
        
        
        #asignamos el usuario despues de haber validado el token
        self.user = user
        
        return attrs
    

    def save(self):
        new_password = self.validated_data['new_password']
        user = self.user

        user.set_password(new_password)
        user.save()

        return user
    


