from apps.permissions.models import Permission

class PermissionSerializer:
    def __init__(self, ids):
        self.ids = ids
        return super().__init__()
    
    def get_permission(self, qs):
        d = {}
        for q in qs:
            d[q.permission] = True
        return d
    
    def data(self):
        permissions = {}
        perms = Permission.objects.filter(id__in=self.ids)
        print(perms)
        groups = list(set(perms.values_list('group', flat=True)))
        print(groups)
        for group in groups:
            print(group)
            perm = perms.filter(group=group)
            permissions[group] = self.get_permission(perm)
        return permissions
            
            