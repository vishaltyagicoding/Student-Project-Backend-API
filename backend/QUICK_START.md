# Quick Start Guide - Student Management System

## ✅ Setup Complete!

Your student management system is now ready with email notifications.

## 🚀 Next Steps

### 1. Start the Development Server

```bash
python manage.py runserver
```

### 2. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 3. Configure Email (Optional but Recommended)

Edit your `.env` file:

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

For development, use console backend (emails print to console):
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### 4. Start Celery Worker (For Email Sending)

```bash
# Windows
celery -A config worker -l info --pool=solo

# Linux/Mac
celery -A config worker -l info
```

### 5. Test Email Configuration

```bash
python manage.py test_email --email your-test@email.com --type simple
```

## 📚 API Endpoints

Base URL: `http://localhost:8000/api/students/`

### Available Endpoints:

- **Branches**: `/api/students/branches/`
- **Courses**: `/api/students/courses/`
- **Colleges**: `/api/students/colleges/`
- **Students**: `/api/students/students/`
- **College Branches**: `/api/students/college-branches/`
- **College Courses**: `/api/students/college-courses/`

### Authentication:

Get JWT token:
```bash
POST /api/auth/login/
{
  "email": "user@example.com",
  "password": "password"
}
```

Use token in headers:
```
Authorization: Bearer <your_access_token>
```

## 🧪 Test the API

### Create a Student:

```bash
POST /api/students/students/
Authorization: Bearer <token>
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "student_id": "STU001"
}
```

**Result**: Student created + Welcome email sent automatically!

### List All Students:

```bash
GET /api/students/students/
Authorization: Bearer <token>
```

### Search Students:

```bash
GET /api/students/students/search/?q=john
Authorization: Bearer <token>
```

## 📧 Email Features

When a student is created:
- ✅ Welcome email sent automatically
- ✅ Contains student ID and college info
- ✅ Processed asynchronously (non-blocking)

When a student is updated:
- ✅ Update notification email sent

Admin bulk email:
```bash
POST /api/students/students/send_bulk_email/
Authorization: Bearer <admin_token>

{
  "student_ids": [1, 2, 3],
  "subject": "Important Announcement",
  "message": "Your message here..."
}
```

## 📖 Documentation

- **API Documentation**: `backend/apps/students/README.md`
- **Email Setup Guide**: `backend/apps/students/EMAIL_SETUP_GUIDE.md`

## 🔧 Troubleshooting

### Migrations not working?
```bash
python manage.py makemigrations
python manage.py migrate
```

### Email not sending?
1. Check Celery worker is running
2. Verify email credentials in `.env`
3. Check logs: `backend/logs/django.log`
4. Use console backend for testing

### Import errors?
```bash
pip install django-filter celery redis django-redis
```

## 🎯 Admin Panel

Access at: `http://localhost:8000/admin/`

Features:
- Manage students, colleges, branches, courses
- Search and filter capabilities
- Bulk actions
- Autocomplete for relationships

## 📊 Database Models

- **Student**: Student information
- **College**: College details
- **Branch**: Academic branches
- **Course**: Course information
- **CollegeBranch**: College-Branch relationships
- **CollegeCourse**: College-Course relationships

## 🔐 Permissions

- **Read**: All authenticated users
- **Create/Update/Delete (Colleges, Branches, Courses)**: Admin only
- **Student Update/Delete**: Owner or Admin

## 💡 Tips

1. Use console email backend during development
2. Start Celery worker before testing emails
3. Check logs for debugging
4. Use the admin panel for quick data management
5. Test with Postman or similar API client

## 🆘 Support

Check the logs:
```bash
tail -f backend/logs/django.log
```

Run system check:
```bash
python manage.py check
```

Test email:
```bash
python manage.py test_email --email test@example.com --type simple
```

---

**Happy Coding! 🚀**
