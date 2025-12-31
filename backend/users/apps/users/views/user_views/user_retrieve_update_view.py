from django.db import transaction

from rest_framework.generics  import RetrieveUpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError


from apps.users.serializers.user_serializers.user_update_serializer import UserUpdateSerializer
from apps.users.serializers.user_serializers.user_serializer import UserSerializer


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        method = self.request.method

        if method == 'GET':
            return UserSerializer

        elif method in ['PUT', 'PATCH']:
            return UserUpdateSerializer


    def update(self, request, *args, **kwargs):

        allowed_fields = self.get_serializer_class().allowed_write_fields
        partial = True

        for field in request.data.keys():
            if field not in allowed_fields:
                raise ParseError(f"El campo {field} no está permitido")


        if request.method == 'PUT':
            missing = []
            for field in allowed_fields:
                if field not in request.data:
                    missing.append(field)

            if not missing:
                partial = False
            
            else:
                raise ParseError(f"Faltan campos obligatorios {', '.join(missing)}")

        instance = request.user

        with transaction.atomic():
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

        user_response = UserSerializer(user)
    
        return Response({'message':'Datos actualizados correctamente', 'data':user_response.data}, status=status.HTTP_200_OK)


