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
        
        auth_header = request.headers.get('Authorization', None)

        try:

            token = auth_header.split() if auth_header and auth_header.startswith('Bearer ') else None

            if token and len(token) > 1:

                claims = jwt.decode(
                    token[1],
                    settings.JWT_PUBLIC_KEY,
                    algorithms=['RS256']
                )

                claims['valid'] = True

                return Response(claims, status=status.HTTP_200_OK)
            
            else:
                return Response({'error':'Token mal formateado'}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.PyJWTError:
            return Response({'error':'Token iválido o expirado'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
