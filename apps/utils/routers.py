from rest_framework.routers import SimpleRouter
from .views import (
    CountryViewSet,
    RegionViewSet,
    CityViewSet,
    TypeGroupViewSet,
    TypeValueViewSet,
    LicenseViewSet,
)

utils_routers = SimpleRouter()
utils_routers.register(r'countries', CountryViewSet, basename='country')
utils_routers.register(r'country/regions', RegionViewSet, basename='regions')
utils_routers.register(r'country/region/cities', CityViewSet, basename='cities')
utils_routers.register(r'types', TypeGroupViewSet, basename='type')
utils_routers.register(r'type/values', TypeValueViewSet, basename='typevalue')
utils_routers.register(r'licenses', LicenseViewSet, basename='license')
