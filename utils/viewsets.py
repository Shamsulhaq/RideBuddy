from django.utils import timezone
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS
from .permissions import HasPermission
from .paginations import LimitPagination


class PubicReadOnlyViewSet(ModelViewSet):
    pagination_class = LimitPagination
    permission_classes = []

    def initial(self, request, *args, **kwargs):
        if self.permission_classes and len(self.permission_classes):
            pass
        elif request.method in SAFE_METHODS:
            self.permission_classes = (permissions.AllowAny,)
        else:
            self.permission_classes = (permissions.IsAdminUser,)
        return super(PubicReadOnlyViewSet, self).initial(request, *args, **kwargs) 


class NoMethodsAllowedViewSet(GenericViewSet):
    serializer_class = []
    queryset = None
    permission_classes = (permissions.AllowAny,)


class PubicReadWriteOnlyViewSet(ModelViewSet):
    pagination_class = LimitPagination
    permission_classes = []

    def initial(self, request, *args, **kwargs):
        if self.permission_classes and len(self.permission_classes):
            pass
        elif request.method in ['POST', 'GET']:
            self.permission_classes = (permissions.IsAuthenticated,)
        else:
            self.permission_classes = (permissions.IsAdminUser,)
        return super(PubicReadWriteOnlyViewSet, self).initial(request, *args, **kwargs) 
    
    
class AuditModelViewSet(ModelViewSet):
    pagination_class = LimitPagination
    permission_classes = (HasPermission, )
    
    def perform_create(self, serializer):
        obj =serializer.save()
        obj.created_by = self.request.user
        obj.created_on = timezone.now()
        obj.save()
        
    
    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.modified_by = request.user
        obj.modified_on = timezone.now()
        obj.save()
        return super(AuditModelViewSet, self).update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """this method will mark instance as destroyed and if it is employee 
            or customer then it will make user as inactive """
        obj = self.get_object()
        obj.deleted_by = request.user
        obj.deleted_on = timezone.now()
        obj.is_deleted = True
        obj.is_active = False
        obj.save()
        _model = type(obj).__name__
        if _model in ['User']:
            obj.user.is_active = False
            obj.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
