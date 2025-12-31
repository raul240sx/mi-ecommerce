from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError

from rest_framework import serializers

from apps.users.tokens.email_verification import EmailVerificationTokenGenerator
from apps.users.models.user import User


class EmailVerificationSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            uid = smart_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(id=uid)


        except (User.DoesNotExist, DjangoUnicodeDecodeError, OverflowError, ValueError, TypeError):
            raise serializers.ValidationError({'detail':'El enlace de restablecimiento es inválido o ha expirado.'})
        
        if user.is_verified == True:
                raise serializers.ValidationError({'detail':'El usuario ya se encuentra verificado'})
    
        token = EmailVerificationTokenGenerator().check_token(user, attrs.get('token'))

        if not token:
            raise serializers.ValidationError({'detail':'El enlace de restablecimiento es inválido o ha expirado.'})

        self.user = user

        return attrs
    
    def save(self):
        self.user.is_verified = True
        self.user.save(update_fields=['is_verified'])

        return self.user
        

