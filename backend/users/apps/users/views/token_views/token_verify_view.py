from django.conf import settings

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.users.permissions.is_internal_service import IsInternalService

import jwt


class TokenVerifyView(APIView):
    authentication_classes = []
    permission_classes = [IsInternalService]


    def post(self, request, *args, **kwargs):
        
        auth_header = request.headers.get('Authorization', '')
        token_str = None

        if auth_header.startswith('Bearer '):
            parts = auth_header.split()
            if len(parts) == 2:
                token_str = parts[1]


        if not token_str:
            token_str = request.COOKIES.get('access_token')


        if not token_str:
            return Response({'valid': False, 'error':'No se ha enviado el token'}, status=status.HTTP_400_BAD_REQUEST)


        try:
            claims = jwt.decode(
                token_str,
                settings.JWT_PUBLIC_KEY,
                algorithms=['RS256']
            )

            claims['valid'] = True

            return Response(claims, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'valid': False, 'error': 'Token expirado'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.PyJWTError:
            return Response({'valid': False, 'error': 'Token iválido'}, status=status.HTTP_401_UNAUTHORIZED)

        
        
