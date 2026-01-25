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
        if not auth_header or not auth_header.startswith("Bearer "):
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