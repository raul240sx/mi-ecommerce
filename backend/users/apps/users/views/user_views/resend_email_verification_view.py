from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle


from apps.users.tasks.email_verification import send_verification_email_task



class ResendEmailVerificationApiView(APIView):
    permission_classes = [IsAuthenticated]

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'register'

    def post(self, request):
        
        if request.user.is_verified:
            return Response({'detail':'La cuenta ya se encuentra verificada'}, status=status.HTTP_400_BAD_REQUEST)

        send_verification_email_task.delay(user_id=request.user.id)

        username = request.user.first_name or request.user.email.split('@')[0]

        return Response({'message':f'{username}, se ha enviado un nuevo enlace de verificación a tu correo.'}, status=status.HTTP_200_OK)

