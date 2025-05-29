from django_filters import rest_framework as filters


class BaseOrderBy(filters.FilterSet):
    order_by = filters.CharFilter(method="order_by_filter")
    created_by = filters.CharFilter(field_name='created_by', lookup_expr='icontains')
    modified_by = filters.CharFilter(field_name='modified_by', lookup_expr='icontains')
    deleted_by = filters.CharFilter(field_name='deleted_by', lookup_expr='icontains')

    def order_by_filter(self, qs, name, value):
        return qs.order_by(value)