from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView



@method_decorator(csrf_exempt, name='dispatch')
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            data = {'refresh': refresh_token}
            serializer = self.get_serializer(data=data)

        else:
            serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        response_data = serializer.validated_data

        token_access = response_data.pop('access', None)

        res = Response(response_data, status=status.HTTP_200_OK)

        if token_access:
            jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
            access_lifetime = jwt_settings.get('ACCESS_TOKEN_LIFETIME').total_seconds()



            if token_access:
                res.set_cookie(
                    key='access_token',
                    value=token_access,
                    httponly=True,
                    secure=True,
                    samesite='None',
                    max_age=access_lifetime,
                    domain=getattr(settings, 'SESSION_COOKIE_DOMAIN', None)
                )


        return res
