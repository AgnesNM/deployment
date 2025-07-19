from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.DeploymentTaskViewSet)
router.register(r'notifications', views.EmailNotificationViewSet)
router.register(r'jobs', views.ProcessingJobViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send-email/', views.send_email_notification, name='send-email'),
    path('process-data/', views.process_data, name='process-data'),
    path('task-status/<str:task_id>/', views.check_task_status, name='task-status'),
    path('cleanup/', views.cleanup_notifications, name='cleanup'),
    path('generate-report/', views.generate_report, name='generate-report'),
    path('health/', views.health_check, name='health-check'),
]