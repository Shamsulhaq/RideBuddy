from django_filters import rest_framework as filters
from utils.filters import BaseOrderBy
from .models import Country, Region, City, TypeGroup, TypeValue, License


class CountryFilter(BaseOrderBy):
    class Meta:
        model = Country
        fields = ('id', 'name', 'code')


class RegionFilter(BaseOrderBy):
    class Meta:
        model = Region
        fields = ('id', 'name', 'country')


class CityFilter(BaseOrderBy):
    class Meta:
        model = City
        fields = ('id', 'name', 'region')


class TypeGroupFilter(BaseOrderBy):
    class Meta:
        model = TypeGroup
        fields = ('id', 'name')


class TypeValueFilter(BaseOrderBy):
    group_name = filters.CharFilter(field_name='group__name', lookup_expr='iexact')
    
    class Meta:
        model = TypeValue
        fields = ('id', 'name', 'group', 'group_name')
        
        
class LicenseFilter(BaseOrderBy):
    class Meta:
        model = License
        fields = ('id', 'is_active', 'is_deleted', 'name', 'license_id', 'previous_name',
                  'license_type', 'description', 'launched_in', 'country', 'region', 'is_live',
                  'is_featured'
        )