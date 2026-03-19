from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class LogoutTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        response = Response({'detail':'Sesion cerrada correctamente'}, status=status.HTTP_200_OK)

        domain = getattr(settings, 'SESSION_COOKIE_DOMAIN', None)

        response.delete_cookie('access_token', domain=domain, path='/')
        response.delete_cookie('refresh_token', domain=domain, path='/')
        response.delete_cookie('csrftoken', domain=domain, path='/')

        return response
