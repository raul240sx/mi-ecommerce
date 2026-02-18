from rest_framework.authentication import BaseAuthentication
from drf_spectacular.extensions import OpenApiAuthenticationExtension


#Autenticación personalizada en base a que en el middleware creado ya se decodifica el token y se extrae el usuario
class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request):
        # El middleware ya procesó el token y asignó el usuario a request._request.user
        user = getattr(request._request, 'user', None)

        if user is not None and getattr(user, 'is_authenticated', False):
            return (user, None)
        
        # Si no hay usuario autenticado, retornar None permite que otros autenticadores lo intenten
        return None
    


class CustomAuthScheme(OpenApiAuthenticationExtension):
    target_class = 'apps.base.custom_authentication.CustomAuthentication'
    name = 'JWTAuth'  # El nombre que aparecerá en Swagger

    def get_security_definition(self, auto_schema):
        # Aquí le decimos a Swagger que el cliente debe enviar un Bearer Token
        # aunque tu middleware sea el que lo procese después.
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }