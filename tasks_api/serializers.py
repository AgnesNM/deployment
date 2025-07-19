from rest_framework import serializers
from .models import EmailNotification, DeploymentTask, ProcessingJob

class EmailNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotification
        fields = ['id', 'recipient', 'subject', 'message', 'sent_at', 'status']
        read_only_fields = ['id', 'sent_at', 'status']

class DeploymentTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeploymentTask
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class ProcessingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingJob
        fields = ['id', 'name', 'status', 'result', 'created_at', 'completed_at']
        read_only_fields = ['id', 'status', 'result', 'created_at', 'completed_at']

# Input serializers for API endpoints
class SendEmailSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()

class ProcessDataSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, default="Data Processing Job")
    data = serializers.ListField(child=serializers.CharField())

class TaskStatusSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    status = serializers.CharField()
    result = serializers.JSONField(required=False)
    successful = serializers.BooleanField(required=False)