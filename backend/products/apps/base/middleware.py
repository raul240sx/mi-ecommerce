import jwt
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
import requests

class UserPayload:
    """Clase auxiliar para simular un objeto de usuario en el request"""
    def __init__(self, payload):
        self.id = payload.get('user_id')
        self.is_authenticated = True
        self.payload = payload

class JWTVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_key = settings.JWT_PUBLIC_KEY
        self.verify_url = settings.USERS_VERIFY_URL

    def __call__(self, request):
        # 1. URLs totalmente exentas (ni siquiera miramos el token)
        exempt_urls = ['/swagger/', '/redoc/', '/admin/', '/media/']
        if any(request.path.startswith(url) for url in exempt_urls):
            return self.get_response(request)

        auth_header = request.headers.get("Authorization")

        # 2. SI NO HAY TOKEN: Lo tratamos como AnonymousUser y DEJAMOS PASAR.
        # Tus permission_classes en el ViewSet decidirán qué hacer con él.
        if not auth_header or not auth_header.startswith("Bearer"):
            request.user = AnonymousUser()
            return self.get_response(request)

        token = auth_header.split(" ")[1]

        # 3. SI HAY TOKEN: Intentamos validarlo localmente
        try:
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=["RS256"]
            )
            # Inyectamos el usuario en el request para que el ViewSet lo use
            request.user = UserPayload(payload)
            return self.get_response(request)

        except jwt.PyJWTError:
            # 4. FALLBACK: Validación remota si la local falla
            try:
                response = requests.post(self.verify_url, json={"token": token}, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("valid"):
                        # Inyectamos los datos del usuario que vienen del microservicio
                        request.user = UserPayload(data.get("user_data", {}))
                        return self.get_response(request)
            except Exception:
                # Si el servicio de usuarios está caído, es un error de infraestructura
                return JsonResponse({"detail": "Auth service unavailable"}, status=503)

        # 5. Si envió un token y fallaron ambas validaciones, es un token corrupto/expirado
        return JsonResponse({"detail": "Invalid or expired token"}, status=401)
    





import requests

from django.contrib.auth.models import AnonymousUser

from django.http import JsonResponse
from django.conf import settings

import jwt

class UserPayload:
    def __init__(self, claims):
        self.id = claims.get('user_id')
        self.is_staff = claims.get('is_staff', False)
        self.is_authenticated = True



class JWTVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.public_key = settings.JWT_PUBLIC_KEY
        self.token_verify_url = settings.TOKEN_VERIFY_URL
        self.internal_service_key = settings.INTERNAL_SERVICE_KEY
        self.try_call_verify = settings.CALL_USERS_SERVICE



    def call_users_service(self, token):
        headers = {'Authorization':f'Bearer {token}',
                    'Internal-Service-Key':self.internal_service_key}
        
        try:
            response = requests.post(self.token_verify_url, headers=headers, timeout=5)

            if response.status_code == 200:
                return response.json()
            
            else:
                return None

        except requests.exceptions.RequestException as e:
            return 'connect_error'


    def __call__(self, request):
        exemt_urls = ['/admin/', '/swagger/', '/redoc/']

        request_url = request.path

        for url in exemt_urls:
            if request_url.startswith(url):
                request.user = AnonymousUser()
                return self.get_response(request)
    
        auth_header = request.headers.get('Authorization', None)

        try:
            token = auth_header.split() if auth_header and auth_header.startswith('Bearer ') else None

            if token and len(token) > 1:
                claims = jwt.decode(
                    token[1],
                    self.public_key,
                    algorithms=['RS256']
                )

                user_data = UserPayload(claims)
                request.user = user_data

                return self.get_response(request)
            
            return JsonResponse({'error':'Token mal formateado'}, status=401)
        
        except jwt.PyJWTError:
            if self.try_call_verify and token and len(token) > 1:
                claims = self.call_users_service(token[1])

                if claims == 'connect_error':
                    return JsonResponse({"detail": "Auth service unavailable"}, status=503)

                
                if claims and claims.get('valid', False):
                    user_data = UserPayload(claims)
                    request.user = user_data

                    return self.get_response(request)


            return JsonResponse({'error':'Token expirado o inválido'}, status=401)
        




