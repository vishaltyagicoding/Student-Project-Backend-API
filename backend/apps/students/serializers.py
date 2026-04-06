from rest_framework import serializers
from .models import Branch, Course, College, CollegeBranch, CollegeCourse, Student


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name', 'code', 'department', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_code(self, value):
        if not value.strip():
            raise serializers.ValidationError("Branch code cannot be empty.")
        return value.upper()


class CourseSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'code', 'branch', 'branch_name', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_code(self, value):
        if not value.strip():
            raise serializers.ValidationError("Course code cannot be empty.")
        return value.upper()


class CollegeBranchSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    branch_code = serializers.CharField(source='branch.code', read_only=True)
    
    class Meta:
        model = CollegeBranch
        fields = ['id', 'college', 'college_name', 'branch', 'branch_name', 'branch_code']
        read_only_fields = ['id']


class CollegeCourseSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    
    class Meta:
        model = CollegeCourse
        fields = ['id', 'college', 'college_name', 'course', 'course_name', 'course_code']
        read_only_fields = ['id']


class CollegeSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)
    branch_count = serializers.SerializerMethodField()
    
    class Meta:
        model = College
        fields = ['id', 'name', 'code', 'address', 'branches', 'branch_count', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_branch_count(self, obj):
        return obj.branches.count()

    def validate_code(self, value):
        if not value.strip():
            raise serializers.ValidationError("College code cannot be empty.")
        return value.upper()


class StudentSerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.name', read_only=True)
    course_name = serializers.CharField(source='course.course.name', read_only=True)
    branch_name = serializers.CharField(source='branch.branch.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 
            'student_id', 'college', 'college_name', 'course', 
            'course_name', 'branch', 'branch_name', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value.lower()

    def validate_student_id(self, value):
        if not value.strip():
            raise serializers.ValidationError("Student ID cannot be empty.")
        return value.upper()

    def validate(self, data):
        # Validate that course belongs to the selected college
        if 'course' in data and 'college' in data:
            if data['course'] and data['college']:
                if data['course'].college != data['college']:
                    raise serializers.ValidationError(
                        "Selected course does not belong to the selected college."
                    )
        
        # Validate that branch belongs to the selected college
        if 'branch' in data and 'college' in data:
            if data['branch'] and data['college']:
                if data['branch'].college != data['college']:
                    raise serializers.ValidationError(
                        "Selected branch does not belong to the selected college."
                    )
        
        return data


class StudentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    college_name = serializers.CharField(source='college.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Student
        fields = ['id', 'full_name', 'email', 'student_id', 'college_name', 'created_at']
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
