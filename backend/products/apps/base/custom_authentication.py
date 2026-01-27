from rest_framework.authentication import BaseAuthentication


#Autenticación personalizada en base a que en el middleware creado ya se decodifica el token y se extrae el usuario
class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request):
        user = getattr(request._request, 'user', None)

        if user and getattr(user, 'is_authenticated', False):
            return (user, None)
        
        return None