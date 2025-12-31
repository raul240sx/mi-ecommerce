from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle

from apps.users.serializers.user_serializers.password_reset_confirm_serializer import PasswordResetConfirmSerializer


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    throttle_classes = [AnonRateThrottle]
    throttle_scope = 'register'

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({'message':'Constraseña actualizada correctamente'}, status=status.HTTP_200_OK)