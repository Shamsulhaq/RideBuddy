from django.db import models

class Permissions(models.TextChoices):
    CREATE = 'create'
    UPDATE = 'update'
    RETRIEVE = 'retrieve'
    DELETE = 'delete'
    ACTION = 'action'
    

class PermissionGroup(models.TextChoices):
    DASHBOARD = 'dashboard'
    REPORT = 'report'
    USER = 'user'
    CONFIGURATION = 'configuration'
    LICENSE = 'license'
    PARTNER = 'partner'
    AREA = 'area'
    ASSET = 'asset'
    UNIT = 'unit'
    INQUIRY = 'inquiry'
    WISH_LIST = 'wish-list'
    

class Roles(models.TextChoices):
    SUPER_ADMIN = 'super-admin'
    ADMIN = 'admin'
    AGENT ='agent'
    OWNER = 'owner'
    CUSTOMER = 'customer'
    