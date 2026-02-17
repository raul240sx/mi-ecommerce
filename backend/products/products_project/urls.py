from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/users/favicon.ico', permanent=True)),
    path('products-api/admin/', admin.site.urls),
    path('products-api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('products-api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('products-api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('products-api/', include('apps.products.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)