from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView



class CustomTokenRefreshView(TokenRefreshView):
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            refresh_token = request.COOKIES.get('refresh_token')

            if refresh_token:

                if hasattr(request.data, '_mutable'):
                    request.data._mutable = True

                request.data['refresh'] = refresh_token

                if hasattr(request.data, '_mutable'):
                    request.data._mutable = False


        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
            access_lifetime = jwt_settings.get('ACCESS_TOKEN_LIFETIME').total_seconds()

            token_access = response.data.pop('access', '')


            if token_access:
                response.set_cookie(
                    key='access_token',
                    value=token_access,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    max_age=access_lifetime
                )   

        return response
