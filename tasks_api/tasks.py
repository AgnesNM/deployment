from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import EmailNotification, ProcessingJob
import time

@shared_task
def send_notification_email(notification_id):
    """
    Send email notification in the background using database record
    """
    try:
        notification = EmailNotification.objects.get(id=notification_id)
        
        # Simulate email processing time
        time.sleep(2)
        
        send_mail(
            subject=notification.subject,
            message=notification.message,
            from_email=settings.DEFAULT_FROM_EMAIL or 'noreply@example.com',
            recipient_list=[notification.recipient],
            fail_silently=False,
        )
        
        notification.status = 'sent'
        notification.save()
        
        return f"Email sent successfully to {notification.recipient}"
        
    except EmailNotification.DoesNotExist:
        return "Email notification not found"
    except Exception as e:
        if 'notification' in locals():
            notification.status = 'failed'
            notification.save()
        return f"Failed to send email: {str(e)}"

@shared_task
def process_deployment_data(job_id, data):
    """
    Process deployment data and update job status
    """
    try:
        job = ProcessingJob.objects.get(id=job_id)
        job.status = 'processing'
        job.save()
        
        # Simulate heavy processing
        time.sleep(10)
        
        # Process the data
        processed_result = {
            'input_data': data,
            'processed_items': len(data) if isinstance(data, list) else 1,
            'processing_time': 10,
            'timestamp': timezone.now().isoformat(),
            'success': True
        }
        
        job.status = 'completed'
        job.result = processed_result
        job.completed_at = timezone.now()
        job.save()
        
        return processed_result
        
    except ProcessingJob.DoesNotExist:
        return {"error": "Processing job not found"}
    except Exception as e:
        if 'job' in locals():
            job.status = 'failed'
            job.result = {"error": str(e)}
            job.save()
        return {"error": str(e)}

@shared_task
def cleanup_old_notifications():
    """
    Clean up old email notifications (older than 30 days)
    """
    from datetime import timedelta
    
    cutoff_date = timezone.now() - timedelta(days=30)
    deleted_count = EmailNotification.objects.filter(
        sent_at__lt=cutoff_date
    ).delete()
    
    return f"Deleted {deleted_count[0]} old notifications"

@shared_task
def generate_deployment_report():
    """
    Generate a deployment status report using real data
    """
    time.sleep(5)  # Simulate report generation
    
    from .models import DeploymentTask
    
    total_tasks = DeploymentTask.objects.count()
    completed_tasks = DeploymentTask.objects.filter(completed=True).count()
    pending_emails = EmailNotification.objects.filter(status='pending').count()
    processing_jobs = ProcessingJob.objects.filter(status='processing').count()
    
    report = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        'pending_emails': pending_emails,
        'processing_jobs': processing_jobs,
        'generated_at': timezone.now().isoformat()
    }
    
    return report