#serializer.py 
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import User
from apps.permissions.choices import Roles
from apps.permissions.models import Permission, UserPermission, RolePermission


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField(read_only=True)
    
    def get_permissions(self, user):
        perms_ids =  user.get_permissions()
        from apps.permissions.serializers import PermissionSerializer
        perms = PermissionSerializer(perms_ids).data()
        return perms

    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'fullname', 'phone', 'role', 'is_active', 'last_active_on', 'permissions')
        read_only_fields = ('email', 'username', 'role', 'is_active', 'last_active_on', 'permissions')


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ("email", "phone", "fullname", "password")
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('email already exists')
        return value

    @transaction.atomic
    def create(self, validated_data, *args, **kwargs):
        password = validated_data.pop("password", None)
        email = validated_data.get("email", None)
        phone = validated_data.get("phone", None)
        fullname = validated_data.get("fullname", None)
        user = User.objects.create(email=email, role=Roles.CUSTOMER)
        user.set_password(password)
        if phone:
            user.phone = phone
        if fullname:
            user.fullname = fullname
        user.save()
        return user

    def update(self, instance, validated_data, *args, **kwargs):
        password = validated_data.pop("password", None)
        instance = super(SignupSerializer, self).update(instance, validated_data, *args, **kwargs)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
    

class AuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={'email': "is required"})
    password = serializers.CharField(required=True, error_messages={'password': "is required"})
    
    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        request = self.context['request']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(
                {
                    "does-not-exist": "user is not exist with this email"
                }
            )

        user = authenticate(username=user.email, password=password)
        if user is None:
            raise ValidationError(
                {
                    "wrong-credentials": "wrong credentials"
                }
            )
        login(request=request, user=user)
        Token.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        data = UserSerializer(user, context={'request': request}).data
        data['token'] = token.key
        return data

class PasswordValidate(serializers.Serializer):
    password = serializers.CharField(required=True, error_messages={'password': "is required"})
    
    def validate_password(self, value):
        validate_password(value)
        return value
    

class UserBioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'fullname', 'username', 'photo', 'role')


class AdminManagedUserSerializer(UserSerializer):
    add_permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True, write_only=True, required=False)
    remove_permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True, write_only=True, required=False)
    
    class Meta:
        model = User
        fields = UserSerializer.Meta.fields+('add_permissions', 'remove_permissions', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        add_permissions = validated_data.pop('add_permissions', [])
        remove_permissions = validated_data.pop('remove_permissions', [])
        password = validated_data.pop('password', None)
        validated_data['is_active'] = validated_data.get('is_active', True)
        if password:
            validated_data["password"] = make_password(password)
        instance = super().create(validated_data)
        if add_permissions:
            permission_instance = UserPermission.objects.create(user=instance)
            for permission in add_permissions:
                permission_instance.permission.add(permission)
        return instance
    
    def update(self, instance, validated_data):
        add_permissions = validated_data.pop('add_permissions', [])
        remove_permissions = validated_data.pop('remove_permissions', [])
        password = validated_data.pop('password', None)
        if password:
            validated_data["password"] = make_password(password)
        if remove_permissions or add_permissions:
            permission_instance, created = UserPermission.objects.get_or_create(user=instance)
            existing_permission_ids = set(permission_instance.permission.values_list('id', flat=True))
            if remove_permissions:
                remove_permissions = Permission.objects.filter(id__in=[p.id for p in remove_permissions]).filter(id__in=existing_permission_ids)
                if remove_permissions.exists():
                    permission_instance.permission.remove(*remove_permissions)
                existing_permission_ids = set(permission_instance.permission.values_list('id', flat=True))
            if add_permissions:
                new_permissions = Permission.objects.filter(id__in=[p.id for p in add_permissions]).exclude(id__in=existing_permission_ids)
                if new_permissions.exists():
                    permission_instance.permission.add(*new_permissions)
        return super().update(instance, validated_data)
    