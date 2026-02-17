# backend/users/users_project/urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/users/favicon.ico', permanent=True)),
    path('users-api/admin/', admin.site.urls),
    path('users-api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('users-api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('users-api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('users-api/', include('apps.users.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)