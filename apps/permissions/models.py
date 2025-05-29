from django.db import models
from django.contrib.auth import get_user_model
# from django.contrib.auth.models import Permission
from .choices import Roles, Permissions, PermissionGroup

User = get_user_model()

class Permission(models.Model):
    permission = models.CharField(max_length=20, choices=Permissions.choices)
    group = models.CharField(max_length=50, choices=PermissionGroup.choices)
    
    def __str__(self):
        return f"{self.group.title()} - [{self.permission.title()}]"

    class Meta:
        unique_together = ['permission', 'group']


class RolePermission(models.Model):
    role = models.CharField(max_length=30, choices=Roles.choices)
    permission = models.ManyToManyField(Permission, blank=True, related_name="role_permissions", related_query_name="role")

    def __str__(self):
        return self.role


class UserPermission(models.Model):
    """This allows overriding permissions for a specific user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ManyToManyField(Permission, blank=True, related_name="user_permissions", related_query_name="user")

    def __str__(self):
        return f"{self.user}"
    

