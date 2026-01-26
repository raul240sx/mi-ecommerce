import secrets

from django.conf import settings

from rest_framework.permissions import BasePermission


class IsInternalService(BasePermission):
    
    def has_permission(self, request, view):

        recieved_key = request.headers.get('Internal-Service-Key', '')
        expected_key = settings.INTERNAL_SERVICE_KEY

        return secrets.compare_digest(recieved_key, expected_key)
