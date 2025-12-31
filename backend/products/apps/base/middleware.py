import jwt
from django.http import JsonResponse
from django.conf import settings
import requests

class JWTVerificationMiddleware:
    """
    Middleware que:
    - Verifica localmente el token RS256 usando la clave pública.
    - Si falla, consulta al users-service.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.public_key = settings.JWT_PUBLIC_KEY
        self.verify_url = settings.USERS_VERIFY_URL

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse({"detail": "Missing or invalid Authorization header"}, status=401)

        token = auth_header.split(" ")[1]

        # 1) Validación local usando la clave pública
        try:
            jwt.decode(
                token,
                self.public_key,
                algorithms=["RS256"]
            )
            return self.get_response(request)  # token válido localmente

        except jwt.PyJWTError:
            pass  # si falla, se intenta validación remota

        # 2) Validación remota usando users-service
        try:
            response = requests.post(self.verify_url, json={"token": token})

            if response.status_code == 200 and response.json().get("valid"):
                return self.get_response(request)

        except Exception:
            return JsonResponse({"detail": "Unable to verify token remotely"}, status=503)

        return JsonResponse({"detail": "Invalid token"}, status=401)
