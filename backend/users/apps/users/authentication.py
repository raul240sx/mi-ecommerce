from datetime import timedelta

from django.utils import timezone
from django.conf import settings

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ExpiringTokenAuthentication(TokenAuthentication):

    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    def is_token_expired (self, token):
        return self.expires_in(token) < timedelta(seconds=0)


    def token_expire_handler(self, token):
        is_expired = self.is_token_expired(token)
        if is_expired:
            print('token expirado')
        return is_expired


    def authenticate_credentials(self,key):
        try:
            token = self.get_model().objects.select_related('user').get(key=key)
        
        except self.get_model().DoesNotExist:
            raise AuthenticationFailed('Token inválido')
        
        if not token.user.is_active:
            raise AuthenticationFailed('Usuario no activo o eliminado')
        
        is_expired = self.token_expire_handler(token)

        if is_expired:
            raise AuthenticationFailed('Su token ha expirado')
        
        return (token.user,token)