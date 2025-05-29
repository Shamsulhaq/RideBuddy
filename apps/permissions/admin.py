from django.contrib import admin
from .models import Permission, RolePermission, UserPermission
# Register your models here.

admin.site.register((Permission, RolePermission, UserPermission))
