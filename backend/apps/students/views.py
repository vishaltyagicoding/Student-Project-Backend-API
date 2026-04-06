from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
import logging
from .models import (
    Branch,Course,
    College, CollegeBranch,
    CollegeCourse, Student)
from .serializers import (
    BranchSerializer, CourseSerializer, CollegeSerializer,
    CollegeBranchSerializer, CollegeCourseSerializer,
    StudentSerializer, StudentListSerializer
)
from .permissions import IsAdminOrReadOnly, IsOwnerOrAdmin

logger = logging.getLogger(__name__)


class BranchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing branches.
    Provides CRUD operations for Branch model.
    """
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'code']
    search_fields = ['name', 'code', 'department']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """Get all courses for a specific branch"""
        branch = self.get_object()
        courses = Course.objects.filter(branch=branch)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing courses.
    Provides CRUD operations for Course model.
    """
    queryset = Course.objects.select_related('branch').all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['branch', 'code']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CollegeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing colleges.
    Provides CRUD operations for College model.
    """
    queryset = College.objects.prefetch_related('branches').all()
    serializer_class = CollegeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code']
    search_fields = ['name', 'code', 'address']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def branches(self, request, pk=None):
        """Get all branches for a specific college"""
        college = self.get_object()
        college_branches = CollegeBranch.objects.filter(college=college).select_related('branch')
        serializer = CollegeBranchSerializer(college_branches, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def courses(self, request, pk=None):
        """Get all courses for a specific college"""
        college = self.get_object()
        college_courses = CollegeCourse.objects.filter(college=college).select_related('course')
        serializer = CollegeCourseSerializer(college_courses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students for a specific college"""
        college = self.get_object()
        students = Student.objects.filter(college=college)
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)


class CollegeBranchViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing college-branch relationships.
    """
    queryset = CollegeBranch.objects.select_related('college', 'branch').all()
    serializer_class = CollegeBranchSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['college', 'branch']
    ordering = ['college__name', 'branch__name']


class CollegeCourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing college-course relationships.
    """
    queryset = CollegeCourse.objects.select_related('college', 'course').all()
    serializer_class = CollegeCourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['college', 'course']
    ordering = ['college__name', 'course__name']


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing students.
    Provides CRUD operations for Student model with advanced filtering.
    """
    queryset = Student.objects.select_related(
        'college', 'course__course', 'branch__branch'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['college', 'course', 'branch', 'student_id']
    search_fields = ['first_name', 'last_name', 'email', 'student_id']
    ordering_fields = ['first_name', 'last_name', 'created_at', 'student_id']
    ordering = ['first_name', 'last_name']

    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer

    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Advanced search endpoint for students
        Query params: q (search term)
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Search query parameter "q" is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        students = self.queryset.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(student_id__icontains=query) |
            Q(college__name__icontains=query)
        )

        page = self.paginate_queryset(students)
        if page is not None:
            serializer = StudentListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_college(self, request):
        """
        Get students grouped by college
        """
        college_id = request.query_params.get('college_id')
        if not college_id:
            return Response(
                {'error': 'college_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        students = self.queryset.filter(college_id=college_id)
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def update_college(self, request, pk=None):
        """
        Update student's college information
        """
        student = self.get_object()
        college_id = request.data.get('college_id')
        
        if not college_id:
            return Response(
                {'error': 'college_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            college = College.objects.get(id=college_id)
            student.college = college
            student.save()
            serializer = self.get_serializer(student)
            return Response(serializer.data)
        except College.DoesNotExist:
            return Response(
                {'error': 'College not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrReadOnly])
    def send_bulk_email(self, request):
        """
        Send bulk email to selected students
        Body: {
            "student_ids": [1, 2, 3],
            "subject": "Email subject",
            "message": "Email message"
        }
        """
        from .tasks import send_bulk_email_to_students
        
        student_ids = request.data.get('student_ids', [])
        subject = request.data.get('subject', '')
        message = request.data.get('message', '')
        
        if not student_ids or not subject or not message:
            return Response(
                {'error': 'student_ids, subject, and message are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        students = Student.objects.filter(id__in=student_ids)
        if not students.exists():
            return Response(
                {'error': 'No students found with provided IDs'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        student_emails = list(students.values_list('email', flat=True))
        
        try:
            send_bulk_email_to_students.delay(student_emails, subject, message)
            return Response({
                'success': True,
                'message': f'Email queued for {len(student_emails)} students'
            })
        except Exception as e:
            logger.error(f"Failed to queue bulk email: {str(e)}")
            return Response(
                {'error': 'Failed to queue email task'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def bulk_create(self, request):
        """
        Create multiple students at once
        Body: {
            "students": [
                {
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "john@example.com",
                    "student_id": "STU001",
                    "college": 1,
                    "course": 1,
                    "branch": 1
                },
                {
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "email": "jane@example.com",
                    "student_id": "STU002",
                    "college": 1,
                    "course": 1,
                    "branch": 1
                }
            ]
        }
        """
        students_data = request.data.get('students', [])
        
        if not students_data:
            return Response(
                {'error': 'students array is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(students_data, list):
            return Response(
                {'error': 'students must be an array'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_students = []
        errors = []
        
        for index, student_data in enumerate(students_data):
            serializer = StudentSerializer(data=student_data)
            if serializer.is_valid():
                try:
                    student = serializer.save()
                    created_students.append({
                        'index': index,
                        'student_id': student.student_id,
                        'email': student.email,
                        'id': student.id
                    })
                except Exception as e:
                    errors.append({
                        'index': index,
                        'data': student_data,
                        'error': str(e)
                    })
            else:
                errors.append({
                    'index': index,
                    'data': student_data,
                    'errors': serializer.errors
                })
        
        response_data = {
            'success': len(created_students),
            'failed': len(errors),
            'created_students': created_students
        }
        
        if errors:
            response_data['errors'] = errors
        
        status_code = status.HTTP_201_CREATED if created_students else status.HTTP_400_BAD_REQUEST
        
        return Response(response_data, status=status_code)

    def perform_create(self, serializer):
        """Override to add custom logic on student creation"""
        serializer.save()

    def perform_update(self, serializer):
        """Override to add custom logic on student update"""
        serializer.save()
