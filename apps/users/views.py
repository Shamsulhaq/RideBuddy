import uuid 
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.validators import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth.password_validation import validate_password

from utils.viewsets import NoMethodsAllowedViewSet, AuditModelViewSet
from utils.paginations import LimitPagination
from apps.permissions.models import Permission
from apps.permissions.permissions import HasPermission
from apps.permissions.choices import PermissionGroup, Roles


from .filters import UserFilter
from .models import User, PasswordRestToken
from .serializers import AuthenticationSerializer, SignupSerializer, UserSerializer, AdminManagedUserSerializer, PasswordValidate


class AuthViewSet(NoMethodsAllowedViewSet):
    @action(url_path='login', methods=['POST'], detail=False)
    def login(self, request, **kwargs):
        serializer = AuthenticationSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data)
    
    @action(url_path='signup', methods=['POST'], detail=False)
    def signup(self, request, **kwargs):
        serializer = SignupSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response({"message": "Signup successful!"})
        
    @action(url_path='forget-password/request', methods=['POST'], detail=False)
    def password_rest_request(self, request, **kwargs):
        email = self.request.data.get('email', None)
        if email is None:
            raise ValidationError('Please provide email address')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError('this email is not a valid user email')
        token = PasswordRestToken.objects.create(user=user, token=uuid.uuid4())
        #todo:: need to work will send token in mail
        return Response({'message': 'mail send successfully'})
    
    # @action(url_path='forget-password/token-verify', methods=['post'], detail=False, permission_classes=(permissions.AllowAny,))
    # def token_verify(self, request, **kwargs):
    #     token = self.request.data.get('token', None)
    #     if token is None:
    #         raise ValidationError('Please provide token')
    #     try:
    #         token = PasswordRestToken.objects.get(token=token)
    #         if token:
    #             return Response({'valid': True})
    #     except ForgetPasswordToken.DoesNotExist:
    #         return Response({'valid': False})
    #     return Response()
    
    @action(url_path='forget-password/change-password', methods=['post'], detail=False)
    def change_password(self, request, **kwargs):
        password = self.request.data.get('password', None)
        token = self.request.data.get('token', None)
        data = {'password': password}
        validate = PasswordValidate(data=data)
        validate.is_valid(raise_exception=True)
        try:
            pass_token= PasswordRestToken.objects.get(token=token)
            user = pass_token.user
            user.set_password(password)
            user.save()
            pass_token.delete()
            return Response({'success': True})
        
        except PasswordRestToken.DoesNotExist:
            raise ValidationError({'token': "invalid or wrong token"})

class UserViewSet(AuditModelViewSet):
    serializer_class = UserSerializer
    pagination_class = LimitPagination
    filterset_class = UserFilter
    # queryset = User.objects.all()
    permission_classes = (HasPermission,)
    permission_group = PermissionGroup.USER
    
    def get_queryset(self):
        qs = User.objects.all()
        user = self.request.user
        if user.is_admin:
            return qs
        else:
            return qs.filter(id=user.id)

    @action(url_path='me', detail=False, methods=['GET'], permission_classes=(IsAuthenticated,))
    def me(self, request, **kwargs):
        user = self.request.user
        return Response(UserSerializer(user, context={'request': request}).data)
    
    @action(url_path='roles', detail=False, methods=['GET'])
    def get_roles(self, request, *args, **kwargs):
        data = [{"key": r[0], "display": r[1]} for r in Roles.choices]
        return Response({'data': data})
    
    @action(url_path='permission-list', detail=False, methods=['GET'])
    def permission_list(self, request, *args, **kwargs):
        permissions = Permission.objects.all().order_by('group').values_list('id', 'group', 'permission')
        data = [{"key": i[0], "display": f"{i[1]}: {i[2]}"} for i in permissions]
        return Response(data, status=status.HTTP_200_OK)

    @action(url_path='create', detail=False, methods=['POST'])
    def create_user(self, request, *args, **kwargs):
        serializer = AdminManagedUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
    @action(url_path='admin-update', detail=True, methods=['PATCH'])
    def admin_update(self, request, *args, **kwargs):
        instance = self.get_object()        
        serializer = AdminManagedUserSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.update(instance, serializer.validated_data)
        return Response(UserSerializer(instance).data, status=status.HTTP_200_OK)
    

