from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import SimpleRouter

from apps.users.views.user_views.user_retrieve_update_view import UserRetrieveUpdateAPIView
from apps.users.views.user_views.user_register_view import UserRegisterAPIView
from apps.users.views.user_views.password_reset_view import PasswordResetView
from apps.users.views.user_views.password_reset_confirm_view import PasswordResetConfirmView
from apps.users.views.user_views.email_verification_view import EmailVerificationView
from apps.users.views.token_views.token_login_view import TokenLoginView
from apps.users.views.address_views.address_viewset import AddressViewset
from apps.users.views.token_views.token_verify_view import TokenVerifyView
from apps.users.views.token_views.logout_view import LogoutTokenView

router = SimpleRouter()
router.register(r'addresses', AddressViewset, basename='address')

urlpatterns = [
    # Router para Viewsets
    path('', include(router.urls)),

    # Autenticación y Registro
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('login/', TokenLoginView.as_view(), name='login'),
    path('logout/', LogoutTokenView.as_view(), name='logout'),
    
    # Perfil y Verificación
    path('me/', UserRetrieveUpdateAPIView.as_view(), name='user-me'),
    path('email-verification/', EmailVerificationView.as_view(), name='email-verification'),

    # Password Management
    path('password-reset/', PasswordResetView.as_view(), name='password-reset-view'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),

    # JWT Tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token-verify/', TokenVerifyView.as_view(), name='token-verify'),
]