from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.users.serializers.user_serializers.email_verification_serializer import EmailVerificationSerializer


class EmailVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
        serializer = EmailVerificationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        username = user.email.split('@')[0]

        return Response({'message':f'Hola {user.first_name or username}, tu cuenta ha sido activada'}, status=status.HTTP_200_OK)

