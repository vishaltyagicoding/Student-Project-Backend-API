from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class APIDocumentationView(TemplateView):
    """
    API Documentation homepage view
    """
    template_name = 'api_documentation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Student Management System - API Documentation'
        return context


@api_view(['GET'])
def api_root(request):
    """
    API Root endpoint - Returns available API endpoints
    """
    return Response({
        'message': 'Welcome to Student Management System API',
        'version': '1.0.0',
        'documentation': request.build_absolute_uri('/'),
        'endpoints': {
            'authentication': {
                'login': request.build_absolute_uri('/api/auth/login/'),
                'register': request.build_absolute_uri('/api/auth/register/'),
                'refresh': request.build_absolute_uri('/api/auth/token/refresh/'),
                'logout': request.build_absolute_uri('/api/auth/logout/'),
            },
            'students': {
                'students': request.build_absolute_uri('/api/students/students/'),
                'colleges': request.build_absolute_uri('/api/students/colleges/'),
                'branches': request.build_absolute_uri('/api/students/branches/'),
                'courses': request.build_absolute_uri('/api/students/courses/'),
                'college_branches': request.build_absolute_uri('/api/students/college-branches/'),
                'college_courses': request.build_absolute_uri('/api/students/college-courses/'),
            }
        }
    })
