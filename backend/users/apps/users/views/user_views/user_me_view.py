from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.users.serializers.user_serializers.user_serializer import UserSerializer


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,*args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
