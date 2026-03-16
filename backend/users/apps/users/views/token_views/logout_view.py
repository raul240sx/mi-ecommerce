from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class LogoutTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        response = Response(
        {'detail':'Sesion cerrada correctamente'},
        status=status.HTTP_200_OK
        )

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')


        return response
