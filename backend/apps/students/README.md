# Students App API Documentation

## Overview
Production-ready Django REST API for managing students, colleges, branches, and courses.

## Installation

1. Install required package:
```bash
pip install django-filter
```

2. Run migrations:
```bash
python manage.py makemigrations students
python manage.py migrate
```

## API Endpoints

### Base URL: `/api/students/`

### 1. Branches
- `GET /api/students/branches/` - List all branches
- `POST /api/students/branches/` - Create branch (Admin only)
- `GET /api/students/branches/{id}/` - Get branch details
- `PUT /api/students/branches/{id}/` - Update branch (Admin only)
- `DELETE /api/students/branches/{id}/` - Delete branch (Admin only)
- `GET /api/students/branches/{id}/courses/` - Get courses for branch

**Filters:** `department`, `code`
**Search:** `name`, `code`, `department`

### 2. Courses
- `GET /api/students/courses/` - List all courses
- `POST /api/students/courses/` - Create course (Admin only)
- `GET /api/students/courses/{id}/` - Get course details
- `PUT /api/students/courses/{id}/` - Update course (Admin only)
- `DELETE /api/students/courses/{id}/` - Delete course (Admin only)

**Filters:** `branch`, `code`
**Search:** `name`, `code`

### 3. Colleges
- `GET /api/students/colleges/` - List all colleges
- `POST /api/students/colleges/` - Create college (Admin only)
- `GET /api/students/colleges/{id}/` - Get college details
- `PUT /api/students/colleges/{id}/` - Update college (Admin only)
- `DELETE /api/students/colleges/{id}/` - Delete college (Admin only)
- `GET /api/students/colleges/{id}/branches/` - Get branches for college
- `GET /api/students/colleges/{id}/courses/` - Get courses for college
- `GET /api/students/colleges/{id}/students/` - Get students for college

**Filters:** `code`
**Search:** `name`, `code`, `address`

### 4. College Branches
- `GET /api/students/college-branches/` - List all college-branch relationships
- `POST /api/students/college-branches/` - Create relationship (Admin only)
- `GET /api/students/college-branches/{id}/` - Get relationship details
- `DELETE /api/students/college-branches/{id}/` - Delete relationship (Admin only)

**Filters:** `college`, `branch`

### 5. College Courses
- `GET /api/students/college-courses/` - List all college-course relationships
- `POST /api/students/college-courses/` - Create relationship (Admin only)
- `GET /api/students/college-courses/{id}/` - Get relationship details
- `DELETE /api/students/college-courses/{id}/` - Delete relationship (Admin only)

**Filters:** `college`, `course`

### 6. Students
- `GET /api/students/students/` - List all students
- `POST /api/students/students/` - Create student
- `GET /api/students/students/{id}/` - Get student details
- `PUT /api/students/students/{id}/` - Update student (Owner/Admin only)
- `DELETE /api/students/students/{id}/` - Delete student (Owner/Admin only)
- `GET /api/students/students/search/?q={query}` - Advanced search
- `GET /api/students/students/by_college/?college_id={id}` - Filter by college
- `PATCH /api/students/students/{id}/update_college/` - Update student's college

**Filters:** `college`, `course`, `branch`, `student_id`
**Search:** `first_name`, `last_name`, `email`, `student_id`

## Authentication

All endpoints require JWT authentication. Include the token in the header:
```
Authorization: Bearer <your_access_token>
```

## Permissions

- **Read operations:** All authenticated users
- **Create/Update/Delete (Branches, Courses, Colleges):** Admin users only
- **Student Update/Delete:** Owner or Admin only

## Example Requests

### Create a Student
```bash
POST /api/students/students/
Content-Type: application/json
Authorization: Bearer <token>

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "student_id": "STU001",
  "college": 1,
  "course": 1,
  "branch": 1
}
```

### Search Students
```bash
GET /api/students/students/search/?q=john
Authorization: Bearer <token>
```

### Filter Students by College
```bash
GET /api/students/students/?college=1
Authorization: Bearer <token>
```

## Features

- ModelViewSet-based views for all CRUD operations
- Advanced filtering and search capabilities
- Custom permissions (IsAdminOrReadOnly, IsOwnerOrAdmin)
- Signal handlers for logging
- Validation for data integrity
- Optimized queries with select_related and prefetch_related
- Pagination support
- Custom actions for specific use cases

## Notes

- All codes (branch, course, college) are automatically converted to uppercase
- Email addresses are automatically converted to lowercase
- Student IDs are automatically converted to uppercase
- Validation ensures course and branch belong to selected college


## Email Notifications

The system automatically sends email notifications for:

### 1. New Student Registration
When a new student is created, they receive a welcome email with:
- Student ID
- Email address
- College name
- Welcome message

### 2. Student Information Update
When student information is updated, they receive a notification email.

### 3. Bulk Email (Admin only)
Admins can send bulk emails to multiple students:

```bash
POST /api/students/students/send_bulk_email/
Content-Type: application/json
Authorization: Bearer <admin_token>

{
  "student_ids": [1, 2, 3],
  "subject": "Important Announcement",
  "message": "Your message here..."
}
```

## Email Configuration

### 1. Configure Email Settings in .env file:

```env
# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### 2. For Gmail:
- Enable 2-factor authentication
- Generate an App Password: https://myaccount.google.com/apppasswords
- Use the App Password in EMAIL_HOST_PASSWORD

### 3. Start Celery Worker:

```bash
# Start Celery worker for processing email tasks
celery -A config worker -l info

# For Windows:
celery -A config worker -l info --pool=solo
```

### 4. Start Celery Beat (for scheduled tasks):

```bash
celery -A config beat -l info
```

## Testing Email Functionality

### Test in Development (Console Backend):

Update settings.py for development:
```python
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

This will print emails to console instead of sending them.

### Test Email Sending:

```python
# Django shell
python manage.py shell

from apps.students.tasks import send_student_registration_email

# Test email task
send_student_registration_email.delay(
    student_id='TEST001',
    student_email='test@example.com',
    student_name='Test User',
    college_name='Test College'
)
```

## Celery Tasks

### Available Tasks:

1. **send_student_registration_email** - Sends welcome email to new students
2. **send_student_update_email** - Sends notification when student info is updated
3. **send_bulk_email_to_students** - Sends bulk emails to multiple students

### Task Features:

- Asynchronous processing (non-blocking)
- Automatic retry on failure (max 3 retries)
- Exponential backoff for retries
- Comprehensive logging
- HTML and plain text email support

## Production Deployment Checklist

- [ ] Configure production email service (SendGrid, AWS SES, etc.)
- [ ] Set up Celery with proper process manager (Supervisor, systemd)
- [ ] Configure Redis for Celery broker
- [ ] Set up email templates with company branding
- [ ] Configure email rate limiting
- [ ] Set up monitoring for email delivery
- [ ] Test email deliverability
- [ ] Configure SPF, DKIM, and DMARC records
- [ ] Set up email bounce handling
- [ ] Configure unsubscribe mechanism (if needed)
