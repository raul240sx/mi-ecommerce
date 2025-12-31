from django.db import transaction
from django.db import IntegrityError

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.users.serializers.user_serializers.user_serializer import UserSerializer
from apps.users.serializers.user_serializers.user_create_serializer import UserCreateSerializer
from apps.users.tasks.email_verification import send_verification_email_task



class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    throttle_classes = [AnonRateThrottle]
    throttle_scope = 'register'



    def perform_create(self, serializer):
        with transaction.atomic():
            try:
                user = serializer.save()
                self.created_user = user

                transaction.on_commit(lambda:send_verification_email_task.delay(user_id=user.id))

            except IntegrityError:
                raise ValidationError({'email': 'No se pudo crear el usuario'})



    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        response_serializer = UserSerializer(self.created_user)

        return Response({
            'message':'Usuario creado correctamente',
            'user':response_serializer.data
            }, status=status.HTTP_201_CREATED) 
        

        