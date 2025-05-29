from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from apps.permissions.choices import Roles


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    fullname = models.CharField(max_length=250, blank=True, null=True)
    photo = models.ImageField(upload_to='users/photos', blank=True, null=True)
    username = models.CharField(max_length=20, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_active_on = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_deleted = models.BooleanField(default=False)
    deleted_on = models.DateTimeField(null=True, blank=True)
    role = models.CharField(max_length=25, choices=Roles.choices, default=Roles.CUSTOMER)
    USERNAME_FIELD = 'email'
    objects = UserManager()
            
    
    def __str__(self) -> str:
        return self.email
    
    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser or self.role == Roles.SUPER_ADMIN or self.role == Roles.ADMIN
    
    def save(self, *args, **kwargs):
        if not self.username:  # Set username only if it's not provided
            base_username = slugify(self.email.split('@')[0])  # Convert email username to a slug
            counter = 1
            username = base_username

            # Ensure uniqueness
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            self.username = username

        super().save(*args, **kwargs)

    def get_permissions(self):
        from apps.permissions.models import UserPermission, RolePermission
        role_permissions = RolePermission.objects.filter(role=self.role).values_list('permission', flat=True)
        user_permissions = UserPermission.objects.filter(user=self).values_list('permission', flat=True)
        permissions = list(set(user_permissions) | set(role_permissions))
        return permissions


class PasswordRestToken(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField()

    
 