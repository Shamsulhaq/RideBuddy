from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.permissions.choices import PermissionGroup
from apps.permissions.permissions import HasPermission
from utils.viewsets import AuditModelViewSet
from .utils import qs_for_admin_or_user
from .choices import TypeGroupName, RequiredFields

from .models import (
    Country,
    Region,
    City,
    TypeGroup,
    TypeValue,
    License,
)
from .serializers import (
    CountrySerializer,
    RegionSerializer,
    CitySerializer,
    TypeGroupSerializer,
    TypeValueSerializer,
    LicenseSerializer,
    LicenseAsChoiceSerializer,
)

from .filters import (
    CountryFilter,
    RegionFilter,
    CityFilter,
    TypeGroupFilter,
    TypeValueFilter,
    LicenseFilter
)



class CountryViewSet(AuditModelViewSet):
    permission_group = PermissionGroup.CONFIGURATION
    public_read_access = True
    serializer_class = CountrySerializer
    filterset_class = CountryFilter

    def get_queryset(self):
        qs = Country.objects.all()
        return qs_for_admin_or_user(qs, self.request.user)
        

class RegionViewSet(AuditModelViewSet):
    permission_group = PermissionGroup.CONFIGURATION
    public_read_access = True
    serializer_class = RegionSerializer
    filterset_class = RegionFilter
    
    def get_queryset(self):
        qs = Region.objects.select_related('country').all()
        return qs_for_admin_or_user(qs, self.request.user)


class CityViewSet(AuditModelViewSet):
    permission_group = PermissionGroup.CONFIGURATION
    public_read_access = True
    serializer_class = CitySerializer
    filterset_class = CityFilter
    
    def get_queryset(self):
        qs = City.objects.select_related('region').all()
        return qs_for_admin_or_user(qs, self.request.user)
    
class TypeGroupViewSet(AuditModelViewSet):
    permission_group = PermissionGroup.CONFIGURATION
    public_read_access = True
    serializer_class = TypeGroupSerializer
    filterset_class = TypeGroupFilter

    def get_queryset(self):
        qs = TypeGroup.objects.all()
        return qs_for_admin_or_user(qs, self.request.user)
    
    @action(url_path='type-group-names', detail=False, methods=['GET'])
    def get_type_group_names(self, request, **kwargs):
        data = [{'display': i[1], 'key': i[0]} for i in TypeGroupName.choices]
        return Response(data)
    
    @action(url_path='required-fields', detail=False, methods=['GET'])
    def get_required_fields(self, request, **kwargs):
        data = [{'display': i[1], 'key': i[0]} for i in RequiredFields.choices]
        return Response(data)


class TypeValueViewSet(AuditModelViewSet):
    permission_group = PermissionGroup.CONFIGURATION
    public_read_access = True
    serializer_class = TypeValueSerializer
    filterset_class = TypeValueFilter

    def get_queryset(self):
        qs = TypeValue.objects.all()
        return qs_for_admin_or_user(qs, self.request.user)


class LicenseViewSet(AuditModelViewSet):
    filterset_class = LicenseFilter
    permission_group = PermissionGroup.CONFIGURATION
    public_read_access = True
    serializer_class = LicenseSerializer

    def get_queryset(self):
        qs = License.objects.all()
        return qs_for_admin_or_user(qs, self.request.user)
    
    @action(detail=False, methods=['GET'], url_path='as-choice', permission_classes=(AllowAny,))
    def as_choice(self, request, **kwargs):
        qs = License.objects.filter(is_live=True)
        serializer = LicenseAsChoiceSerializer(qs, many=True)
        return Response(serializer.data)
    
    