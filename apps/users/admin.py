from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, PasswordRestToken

admin.site.site_header = 'Spaci.io'          
admin.site.site_title = 'Spaci.io Super Admin' 
# Unregister Groups and Permissions
admin.site.unregister(Group)
# admin.site.unregister(Permission)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'username', 'email', 'phone', 'role']
    list_filter = ['role', 'is_deleted', 'is_active']
    search_fields = ['fullname', 'username', 'phone', 'deleted_phone', 'email']

admin.site.register((PasswordRestToken,))

