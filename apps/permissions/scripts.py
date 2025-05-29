from .models import Permission
from .choices import PermissionGroup, Permissions

def create_permission():
    perms = []
    
    # Extracting only the values (not labels) from choices
    for group_value, _ in PermissionGroup.choices:
        for perm_value, _ in Permissions.choices:
            if not Permission.objects.filter(permission=perm_value, group=group_value).exists():
                perms.append(Permission(permission=perm_value, group=group_value))
    
    if perms:
        Permission.objects.bulk_create(perms)

        
            