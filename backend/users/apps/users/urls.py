from django.urls import path
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views.user_views.user_retrieve_update_view import UserRetrieveUpdateAPIView
from apps.users.views.user_views.user_register_view import UserRegisterAPIView
from apps.users.views.user_views.password_reset_view import PasswordResetView
from apps.users.views.user_views.password_reset_confirm_view import PasswordResetConfirmView
from apps.users.views.user_views.email_verification_view import EmailVerificationView



urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user-register'),
    path('me/', UserRetrieveUpdateAPIView.as_view(), name='user-me'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset-view'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('email-verification/', EmailVerificationView.as_view(), name='email-verification'),


    #JWT
    path('token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

]
