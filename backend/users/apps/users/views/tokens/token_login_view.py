from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.serializers.user_serializers.token_login_serializer import TokenLoginSerializer

class TokenLoginView(TokenObtainPairView):
    serializer_class = TokenLoginSerializer