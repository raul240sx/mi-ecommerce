from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.serializers.token_serializers.token_login_serializer import TokenLoginSerializer
from apps.users.permissions.is_not_authenticated import IsNotAuthenticated




@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class TokenLoginView(TokenObtainPairView):
    permissions = [IsNotAuthenticated]

    serializer_class = TokenLoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
            access_lifetime = jwt_settings.get('ACCESS_TOKEN_LIFETIME').total_seconds()
            refresh_lifetime = jwt_settings.get('REFRESH_TOKEN_LIFETIME').total_seconds()


            token_access = response.data.pop('access', '')
            token_refresh = response.data.pop('refresh', '')

            if token_access:
                response.set_cookie(
                    key='access_token',
                    value=token_access,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    max_age=access_lifetime,
                    domain=getattr(settings, 'SESSION_COOKIE_DOMAIN', None)
                )

            if token_refresh:
                response.set_cookie(
                    key='refresh_token',
                    value=token_refresh,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    max_age=refresh_lifetime,
                    domain=getattr(settings, 'SESSION_COOKIE_DOMAIN', None)
                )      
            
        return response
