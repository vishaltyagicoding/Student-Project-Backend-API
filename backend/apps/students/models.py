from django.db import models

# Create your models here.
# first model is Branch
class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # Changed from IntegerField to CharField
    department = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Branches"
        verbose_name = "Branch"
        ordering = ['name']


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)  # Changed from SET_DEFAULT
    code = models.CharField(max_length=10, unique=True)  # Changed from IntegerField to CharField
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class College(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    address = models.TextField()
    branches = models.ManyToManyField(Branch, through='CollegeBranch')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Colleges"
        verbose_name = "College"


class CollegeBranch(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.college.name} - {self.branch.name}"
    
    class Meta:
        verbose_name_plural = "College Branches"
        verbose_name = "College Branch"
        unique_together = ['college', 'branch']  # Prevent duplicate relationships


class CollegeCourse(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.college.name} - {self.course.name}"
    
    class Meta:
        verbose_name_plural = "College Courses"
        verbose_name = "College Course"
        unique_together = ['college', 'course']  # Prevent duplicate relationships


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    student_id = models.CharField(max_length=20, unique=True)
    college = models.ForeignKey(College, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(CollegeCourse, on_delete=models.SET_NULL, null=True, blank=True)
    branch = models.ForeignKey(CollegeBranch, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Fixed: was returning self.name which doesn't exist
    
    class Meta:
        verbose_name_plural = "Students"
        verbose_name = "Student"
        ordering = ['first_name', 'last_name']