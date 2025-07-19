from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from .models import EmailNotification, DeploymentTask, ProcessingJob
from .serializers import (
    EmailNotificationSerializer, 
    DeploymentTaskSerializer, 
    ProcessingJobSerializer,
    SendEmailSerializer,
    ProcessDataSerializer,
    TaskStatusSerializer
)
from .tasks import (
    send_notification_email, 
    process_deployment_data, 
    cleanup_old_notifications,
    generate_deployment_report
)

class DeploymentTaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing deployment tasks
    """
    queryset = DeploymentTask.objects.all()
    serializer_class = DeploymentTaskSerializer
    permission_classes = [AllowAny]

class EmailNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing email notifications
    """
    queryset = EmailNotification.objects.all()
    serializer_class = EmailNotificationSerializer
    permission_classes = [AllowAny]

class ProcessingJobViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing processing jobs
    """
    queryset = ProcessingJob.objects.all()
    serializer_class = ProcessingJobSerializer
    permission_classes = [AllowAny]

@extend_schema(
    request=SendEmailSerializer,
    responses={202: {"description": "Email queued for sending"}},
    description="Send an email notification using Celery background task"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def send_email_notification(request):
    """Send email notification asynchronously"""
    serializer = SendEmailSerializer(data=request.data)
    if serializer.is_valid():
        notification = EmailNotification.objects.create(
            recipient=serializer.validated_data['recipient'],
            subject=serializer.validated_data['subject'],
            message=serializer.validated_data['message']
        )
        
        task = send_notification_email.delay(notification.id)
        
        return Response({
            'message': 'Email queued for sending',
            'notification_id': notification.id,
            'task_id': task.id
        }, status=status.HTTP_202_ACCEPTED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    request=ProcessDataSerializer,
    responses={202: {"description": "Data processing started"}},
    description="Process deployment data in the background"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def process_data(request):
    """Process data asynchronously"""
    serializer = ProcessDataSerializer(data=request.data)
    if serializer.is_valid():
        job = ProcessingJob.objects.create(
            name=serializer.validated_data.get('name', 'Data Processing Job')
        )
        
        task = process_deployment_data.delay(
            job.id, 
            serializer.validated_data['data']
        )
        
        return Response({
            'message': 'Data processing started',
            'job_id': job.id,
            'task_id': task.id
        }, status=status.HTTP_202_ACCEPTED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    responses={200: TaskStatusSerializer},
    description="Check the status of a Celery task"
)
@api_view(['GET'])
@permission_classes([AllowAny])
def check_task_status(request, task_id):
    """Check Celery task status"""
    from deployment_project.celery import app
    
    task = app.AsyncResult(task_id)
    
    response_data = {
        'task_id': task_id,
        'status': task.status,
        'result': task.result if task.ready() else None,
        'successful': task.successful() if task.ready() else None
    }
    
    return Response(response_data)

@extend_schema(
    responses={202: {"description": "Cleanup started"}},
    description="Start cleanup of old email notifications"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def cleanup_notifications(request):
    """Start cleanup of old notifications"""
    task = cleanup_old_notifications.delay()
    
    return Response({
        'message': 'Cleanup task started',
        'task_id': task.id
    }, status=status.HTTP_202_ACCEPTED)

@extend_schema(
    responses={202: {"description": "Report generation started"}},
    description="Generate deployment status report"
)
@api_view(['POST'])
@permission_classes([AllowAny])
def generate_report(request):
    """Generate deployment report"""
    task = generate_deployment_report.delay()
    
    return Response({
        'message': 'Report generation started',
        'task_id': task.id
    }, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """Simple health check endpoint"""
    return Response({
        'status': 'healthy',
        'timestamp': timezone.now().isoformat(),
        'service': 'deployment-project',
        'database': 'connected',
        'celery': 'configured'
    })