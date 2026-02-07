from django.urls import path, include

from rest_framework.routers import SimpleRouter

from apps.products.views import ProductViewSet, CategoryViewSet, MeasureUnitViewSet, ReserveStockView



router = SimpleRouter()

router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'measure_units', MeasureUnitViewSet, basename='measure_unit')


urlpatterns = [
    path('', include(router.urls)),
    path('reserve-stock/', ReserveStockView.as_view(), name='reserve-stock')
    
]

