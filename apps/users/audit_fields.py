from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AuditFieldModel(models.Model):
    created_by = models.ForeignKey(User, related_name="%(class)s_created_by", on_delete=models.SET_NULL,blank=True, null=True)
    created_on = models.DateTimeField(null=True, blank=True)
    modified_by = models.ForeignKey(User, related_name="%(class)s_modified_by", on_delete=models.SET_NULL,blank=True, null=True)
    modified_on = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(User, related_name="%(class)s_deleted_by", on_delete=models.SET_NULL,blank=True, null=True)
    deleted_on = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
        

class AuditStatusFieldsModel(AuditFieldModel):
    is_active = models.BooleanField(default=bool(True))
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
        
    def save(self, **kwargs):
        if self.pk is None:
            self.is_active = True
        return super().save(**kwargs)
