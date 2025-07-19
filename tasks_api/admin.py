from django.contrib import admin
from .models import EmailNotification, DeploymentTask, ProcessingJob

@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'subject', 'status', 'sent_at']
    list_filter = ['status', 'sent_at']
    search_fields = ['recipient', 'subject']

@admin.register(DeploymentTask)
class DeploymentTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'completed', 'created_at', 'updated_at']
    list_filter = ['completed', 'created_at']
    search_fields = ['title', 'description']

@admin.register(ProcessingJob)
class ProcessingJobAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name']