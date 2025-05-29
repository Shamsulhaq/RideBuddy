from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import RolePermission, UserPermission, Permission
from .choices import Permissions
  
class HasPermission(BasePermission):
    """
    Custom permission to check if the user has the appropriate permission
    assigned via RolePermission or UserPermission.
    """

    def has_permission(self, request, view):
        # has pubic readable content. 
        public_read_access = getattr(view, 'public_read_access', False)
        if public_read_access and request.method in SAFE_METHODS:
            return True
        
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return False
            
        permission_group = getattr(view, 'permission_group', None)
        if permission_group is None:
            return False
        is_action = hasattr(view, 'action') and view.action not in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy'] and request.method == 'PATCH'
        method_permission_map = {
            'GET': (Permissions.RETRIEVE, permission_group),
            'POST': (Permissions.CREATE, permission_group),
            'PUT': (Permissions.UPDATE, permission_group),
            'PATCH': (Permissions.ACTION, permission_group) if is_action else (Permissions.UPDATE, permission_group),
            'DELETE': (Permissions.DELETE, permission_group),
        }
        
        required_permission, required_group = method_permission_map.get(request.method, (None, None))
        
        if not required_permission or not required_group:
            return True  # Allow access if no specific permission is required
        
        user = request.user
        
        # Check user-specific permissions
        user_permissions = UserPermission.objects.filter(user=user).values_list('permission__permission', 'permission__group')
        if (required_permission, required_group) in user_permissions:
            return True
        
        # Check role-based permissions
        role_permissions = RolePermission.objects.filter(role=user.role).values_list('permission__permission', 'permission__group')
        return (required_permission, required_group) in role_permissions
    