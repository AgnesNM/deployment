"""
URL configuration for deployment_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def home(request):
    return HttpResponse("""
    <h1>Django Deployment Project API</h1>
    <p>Your Django app is running successfully!</p>
    <ul>
        <li><a href="/swagger/">Swagger API Documentation</a></li>
        <li><a href="/api/health/">Health Check</a></li>
        <li><a href="/admin/">Django Admin</a></li>
        <li><a href="/api/">API Endpoints</a></li>
    </ul>
    """)

urlpatterns = [
    path('', home, name='home'),  # Add this line for the root URL
    path('admin/', admin.site.urls),
    path('api/', include('tasks_api.urls')),
    
    # API Schema and Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]