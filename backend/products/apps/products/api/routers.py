from rest_framework.routers import DefaultRouter

from apps.products.api.views.general_views import MeasureUnitViewSet, IndicatorViewSet, CategoryProductViewSet
from apps.products.api.views.product_viewsets import ProductViewSet

router = DefaultRouter()

router.register(r'products',ProductViewSet,basename='products')
router.register(r'measure_unit',MeasureUnitViewSet,basename='measure_unit')
router.register(r'indicators',IndicatorViewSet,basename='indicators')
router.register(r'category_product',CategoryProductViewSet,basename='category_product')


urlpatterns = router.urls