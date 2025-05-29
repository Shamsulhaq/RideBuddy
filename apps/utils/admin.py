from django.contrib import admin
from .choices import TypeGroupName
from .models import (
    City,
    Country,
    License,
    Region,
    TypeGroup,
    TypeValue,
)

admin.site.register((
    City,
    Country,
    Region,
    TypeGroup,
))


@admin.register(TypeValue)
class TypeValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'name')
    list_filter = ('group',)
    search_fields = ('name',)
    class Meta:
        model = TypeValue


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'license_type', 'country','region')
    list_filter = ('region', 'country')
        
