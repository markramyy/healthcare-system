"""
URL configuration for config project.

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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.permissions import AllowAny
from healthcare_ms.core.views import landing_page
from django.contrib.auth import views as auth_views
from config.health import health_check
from django_prometheus import exports

views_patterns = [
    path('dashboard/', include('healthcare_ms.core.urls')),
    path('users/', include('healthcare_ms.users.urls')),
    path('patient/', include('healthcare_ms.patient.urls')),
    path('ehr/', include('healthcare_ms.ehr.urls')),
    path('appointment/', include('healthcare_ms.appointment.urls')),
    path('billing/', include('healthcare_ms.billing.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

urlpatterns = [
    path('', landing_page, name='landing'),
    path('admin/', admin.site.urls),
    path('views/', include(views_patterns)),

    # Health check and monitoring endpoints
    path('health/', health_check, name='health-check'),
    path('metrics/', exports.ExportToDjangoView, name='prometheus-metrics'),

    # Authentication
    path('auth/', include('config.auth_router')),

    # API endpoints
    path('users/', include('healthcare_ms.users.api_router')),
    path('patient/', include('healthcare_ms.patient.api_router')),
    path('ehr/', include('healthcare_ms.ehr.api_router')),
    path('appointment/', include('healthcare_ms.appointment.api_router')),
    path('billing/', include('healthcare_ms.billing.api_router')),

    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema', permission_classes=[AllowAny]), name='api-docs'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='api-schema'), name='redoc'),
]
