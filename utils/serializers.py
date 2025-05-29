from rest_framework import serializers
from apps.users.audit_fields import AuditStatusFieldsModel
from apps.users.serializers import UserBioSerializer


class CommonFieldSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)
    modified_by = serializers.SerializerMethodField(read_only=True)
    deleted_by = serializers.SerializerMethodField(read_only=True)
    
    def get_created_by(self, obj):
        if self.is_retrieve():
            return UserBioSerializer(obj.created_by).data if obj.created_by else None
        else:
            return obj.created_by.pk if obj.created_by else None
        
    def get_modified_by(self, obj):
        if self.is_retrieve():
            return UserBioSerializer(obj.modified_by).data if obj.modified_by else None
        else:
            return obj.modified_by.pk if obj.modified_by else None
        
    def get_deleted_by(self, obj):
        if self.is_retrieve():
            return UserBioSerializer(obj.deleted_by).data if obj.deleted_by else None
        else:
            return obj.deleted_by.pk if obj.deleted_by else None
        
    class Meta:
        model = AuditStatusFieldsModel
        fields = ('created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_by', 'deleted_on', 'is_active', 'is_deleted')
        read_only_fields = ('created_by', 'created_on', 'modified_by', 'modified_on', 'deleted_by', 'deleted_on')
    
    
    def is_retrieve(self):
        """
        Check if the current request is a retrieve call.
        """
        view = self.context.get('view', None)
        if view and hasattr(view, 'action'):
            return view.action == 'retrieve'
        return False

    def is_list(self):
        """
        Check if the current request is a list call.
        """
        view = self.context.get('view', None)
        if view and hasattr(view, 'action'):
            return view.action == 'list'
        return False
    
    def get_user(self):
        view = self.context.get('view', None)
        if view and hasattr(view, 'request'):
            return view.request.user
        return None

    