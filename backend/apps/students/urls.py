from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BranchViewSet,
    CourseViewSet,
    CollegeViewSet,
    CollegeBranchViewSet,
    CollegeCourseViewSet,
    StudentViewSet
)

app_name = 'students'

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'branches', BranchViewSet, basename='branch')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'colleges', CollegeViewSet, basename='college')
router.register(r'college-branches', CollegeBranchViewSet, basename='college-branch')
router.register(r'college-courses', CollegeCourseViewSet, basename='college-course')
router.register(r'students', StudentViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
]
