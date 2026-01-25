from django.urls import path, include

from rest_framework.routers import SimpleRouter

from apps.products.views.product_viewset import ProductViewSet
from apps.products.views.category_viewset import CategoryViewSet
from apps.products.views.measure_unit_viewset import MeasureUnitViewSet


router = SimpleRouter()

router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'measure_units', MeasureUnitViewSet, basename='measure_unit')


urlpatterns = [
    path('', include(router.urls)),
]

