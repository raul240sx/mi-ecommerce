from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle

from apps.users.tasks.password_reset import password_reset_task
from apps.users.serializers.user_serializers.password_reset_serializer import PasswordResetSerializer




@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    throttle_classes = [AnonRateThrottle]
    throttle_scope = 'password_reset'


    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user_id = serializer.save()

        if user_id:
            password_reset_task.delay(user_id=user_id)

        response_message = 'Si el email existe se enviará un correo con el link para el cambio de contraseña'
        return Response({'message':response_message}, status=status.HTTP_200_OK)





