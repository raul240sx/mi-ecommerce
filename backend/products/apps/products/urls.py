from django.urls import path, include

from rest_framework.routers import SimpleRouter

from apps.products.views.product_viewset import ProductViewSet



router = SimpleRouter()

router.register(r'', ProductViewSet, basename='product')


urlpatterns = [
    path('products/', include(router.urls)),

]

