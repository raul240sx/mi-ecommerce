from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('orders-api/', include('apps.orders.urls'))
]
