from rest_framework_simplejwt.views import TokenObtainPairView
from backend.users.apps.users.serializers.token_serializers.token_login_serializer import TokenLoginSerializer

class TokenLoginView(TokenObtainPairView):
    serializer_class = TokenLoginSerializer