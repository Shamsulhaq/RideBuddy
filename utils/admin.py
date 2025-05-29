from django.contrib import admin

class SMSModelAdmin(admin.ModelAdmin):
    actions = ['mark_as_deleted', 'mark_as_active']  # Register the custom action

    def mark_as_deleted(self, request, queryset):
        updated = queryset.update(is_deleted=True, is_active=False)  # Modify field as needed
        self.message_user(request, f"{updated} items marked as Deleted.")
    mark_as_deleted.short_description = "Mark selected as Deleted"
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(is_deleted=False, is_active=True)  # Modify field as needed
        self.message_user(request, f"{updated} items marked as Active.")
    mark_as_active.short_description = "Mark selected as Active"