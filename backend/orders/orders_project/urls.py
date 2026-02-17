from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/users/favicon.ico', permanent=True)),
    path('orders-api/admin/', admin.site.urls),
    path('orders-api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('orders-api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('orders-api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('orders-api/', include('apps.orders.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)