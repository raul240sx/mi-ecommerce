from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.locations.views.commune_viewset import CommuneViewSet
from apps.locations.views.region_viewset import RegionViewSet


router = SimpleRouter()
router.register(r'regions', RegionViewSet, basename='regions')
router.register(r'communes', CommuneViewSet, basename='communes')


urlpatterns = [
    path('', include(router.urls)),
]
