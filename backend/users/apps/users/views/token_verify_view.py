from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import UntypedToken
import jwt
from django.conf import settings

class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response({"valid": False}, status=status.HTTP_400_BAD_REQUEST)

        try:
            UntypedToken(token) 
            jwt.decode(
                token,
                settings.JWT_PUBLIC_KEY,
                algorithms=["RS256"]
            )
            return Response({"valid": True})

        except Exception:
            return Response({"valid": False}, status=status.HTTP_401_UNAUTHORIZED)
