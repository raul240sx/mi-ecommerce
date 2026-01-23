from rest_framework.permissions import BasePermission


class IsStaffPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        is_staff = getattr(user, 'is_staff', None)
        if user.is_authenticated and is_staff:
            return True
        
        return False