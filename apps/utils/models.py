from django.db import models
from apps.users.audit_fields import AuditStatusFieldsModel

from .choices import RequiredFields, TypeGroupName
from utils.utils import get_year_choices


class Country(AuditStatusFieldsModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, help_text="Country Code")
    phone_number_code = models.CharField(max_length=6)
    vat_rate = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

    
class Region(AuditStatusFieldsModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='regions')
    name = models.CharField(max_length=100)
    housing_fees = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
    
    
class City(AuditStatusFieldsModel):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class TypeGroup(AuditStatusFieldsModel):
    name = models.CharField(max_length=250, choices=TypeGroupName.choices, unique=True)
    required_field = models.CharField(max_length=20, choices=RequiredFields.choices, blank=True, null=True)
    
    def __str__(self):
        return self.name


class TypeValue(AuditStatusFieldsModel):
    group = models.ForeignKey(TypeGroup, on_delete=models.CASCADE, related_name='types', related_query_name='type') 
    name = models.CharField(max_length=250)
    icon = models.ImageField(blank=True, null=True)
    percentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return self.name
    

class License(AuditStatusFieldsModel):
    name = models.CharField(max_length=250)
    license_id = models.CharField(max_length=250, unique=True)
    previous_name = models.CharField(max_length=250, blank=True, null=True)
    license_type = models.ForeignKey(TypeValue, on_delete=models.CASCADE, related_name='licenses')
    description = models.TextField(blank=True, null=True)
    launched_in = models.PositiveSmallIntegerField(choices=get_year_choices, blank=True, null=True)
    icon = models.ImageField(upload_to='license/icons', blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='licenses')
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='licenses')
    location_map = models.ImageField(upload_to='license/location-map', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    is_live = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name



    