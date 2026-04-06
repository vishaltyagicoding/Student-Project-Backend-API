from django.contrib import admin
from .models import Branch, Course, College, CollegeBranch, CollegeCourse, Student


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department', 'created_at']
    list_filter = ['department', 'created_at']
    search_fields = ['name', 'code', 'department']
    ordering = ['name']
    readonly_fields = ['created_at']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'branch', 'created_at']
    list_filter = ['branch', 'created_at']
    search_fields = ['name', 'code']
    ordering = ['name']
    readonly_fields = ['created_at']


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'code', 'address']
    ordering = ['name']
    readonly_fields = ['created_at']
    filter_horizontal = ['branches']


@admin.register(CollegeBranch)
class CollegeBranchAdmin(admin.ModelAdmin):
    list_display = ['college', 'branch']
    list_filter = ['college', 'branch']
    search_fields = ['college__name', 'branch__name']
    ordering = ['college__name', 'branch__name']


@admin.register(CollegeCourse)
class CollegeCourseAdmin(admin.ModelAdmin):
    list_display = ['college', 'course']
    list_filter = ['college', 'course']
    search_fields = ['college__name', 'course__name']
    ordering = ['college__name', 'course__name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'email', 'college', 'created_at']
    list_filter = ['college', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'student_id', 'college__name']
    ordering = ['first_name', 'last_name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'student_id')
        }),
        ('Academic Information', {
            'fields': ('college', 'course', 'branch')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter course and branch dropdowns based on selected college"""
        if db_field.name == "course":
            # Get college from URL or form data
            college_id = request.GET.get('college')
            if college_id:
                kwargs["queryset"] = CollegeCourse.objects.filter(college_id=college_id)
            else:
                kwargs["queryset"] = CollegeCourse.objects.all()
        
        if db_field.name == "branch":
            # Get college from URL or form data
            college_id = request.GET.get('college')
            if college_id:
                kwargs["queryset"] = CollegeBranch.objects.filter(college_id=college_id)
            else:
                kwargs["queryset"] = CollegeBranch.objects.all()
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
