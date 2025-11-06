"""
URL configuration for college_erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="College ERP API",
        default_version='v1',
        description="API documentation for the College ERP system",
        contact=openapi.Contact(email="contact@collegeerp.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_app.urls')),
    path('api/students/', include('students.urls')),
    path('api/faculty/', include('faculty.urls')),
    path('api/finance/', include('finance.urls')),
    path('api/admissions/', include('admissions.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/examination/', include('examination.urls')),
    path('api/timetable/', include('timetable.urls')),
    path('api/hostel/', include('hostel.urls')),
    path('api/library/', include('library.urls')),
    path('api/transport/', include('transport.urls')),
    path('api/payroll/', include('payroll.urls')),
    path('api/placements/', include('placements.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/workflow/', include('workflow.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
