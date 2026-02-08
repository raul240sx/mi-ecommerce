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
        exemt_urls = ['/admin/', '/swagger/', '/redoc/', '/orders/webhook/']

        request_url = request.path

        for url in exemt_urls:
            if request_url.startswith(url):
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
                       
            request.user = AnonymousUser()
            return self.get_response(request)
        
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
        




