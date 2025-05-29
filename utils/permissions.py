from rest_framework import permissions
from apps.permissions.permissions import HasPermission


class IsSuperAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.is_superadmin

class IsSuperAdminOrAdmin(IsSuperAdmin):
    def has_permission(self, request, view):
        return IsSuperAdmin.has_permission or request.user.is_admin


class Is_AuthorizeOrReadonly(permissions.BasePermission):
    # super admin admin account admin and agrnt are allowed to create
    def has_object_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.is_superadmin or request.user.is_admin or request.user.is_account_admin


class RoleBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        allowed_roles_to_create = getattr(view, 'allowed_to_create', None)
        allowed_roles_to_edit = getattr(view, 'allowed_to_edit', None)
        allowed_roles_to_delete = getattr(view, 'allowed_to_delete', None)
        allowed_roles =  getattr(view, 'allowed_roles', None)
        if request.method in permissions.SAFE_METHODS:
            if not request.user.is_authenticated:
                return False
            return True
        # elif allowed_roles is not None:
        #     return request.user.role in allowed_roles
        elif request.method == 'POST':
            if allowed_roles_to_create is None:
                return request.user.has_admin_permission or request.user.role in allowed_roles
            return request.user.role in allowed_roles_to_create or request.user.role in allowed_roles
        
        elif request.method in ['PUT', 'PATCH']:
            if allowed_roles_to_edit is None:
                return request.user.has_admin_permission or request.user.role in allowed_roles
            return request.user.role in allowed_roles_to_edit or request.user.role in allowed_roles
        
        elif request.method == 'DELETE':
            if allowed_roles_to_delete is None:
                return request.user.has_admin_permission or request.user.role in allowed_roles
            return request.user.role in allowed_roles_to_delete or request.user.role in allowed_roles
        else:
            return request.user.role in allowed_roles

    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     return request.is_superadmin or request.user.is_admin or request.user == obj
        


# class IsCreatorOrAdminOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission to only allow creators and admin of an object to edit it.
#     """

#     def has_object_permission(self, request, view, obj):
#         # SAFE_METHODS are GET, HEAD, OPTIONS (Read-only methods)
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         # Write permission is only allowed to the creator of the object
#         return obj.user == request.user or request.user.is_admin


# class IsCustomerOrAdmin(permissions.BasePermission):
    
#     def has_permission(self, request, view):
#         return request.user.is_admin or request.user.is_customer


# class IsStaffOrAdmin(permissions.BasePermission):
    
#     def has_permission(self, request, view):
#         return request.user.is_admin or request.user.is_staff_user


# class IsStaffOrAdminOrCustomer(permissions.BasePermission):
    
#     def has_permission(self, request, view):
#         return request.user.is_admin or request.user.is_staff_user or request.user.is_customer


# class IsCustomer(permissions.BasePermission):

#     def has_permission(self, request, view):
#         return request.user.is_customer
    

# class IsStaff(permissions.BasePermission):
    
#     def has_permission(self, request, view):
#         return request.user.is_staff_user