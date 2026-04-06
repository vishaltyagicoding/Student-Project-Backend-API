# Student Management System - API Documentation

## 🌐 Access Documentation

### Live Documentation Homepage
Visit: **http://127.0.0.1:8000/** (when server is running)

The homepage provides:
- Complete API endpoint documentation
- Request/response examples
- Authentication guide
- Interactive examples
- Best practices

### API Root Endpoint
Visit: **http://127.0.0.1:8000/api/**

Returns JSON with all available endpoints and their URLs.

## 🚀 Quick Start

### 1. Start the Server

```bash
cd backend
python manage.py runserver
```

### 2. Access Documentation

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

### 3. Test with Postman

Import the Postman collection:
```
File: Student_Management_API.postman_collection.json
```

Steps:
1. Open Postman
2. Click "Import"
3. Select the JSON file
4. Collection will be imported with all endpoints

## 📋 Available Endpoints

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/logout/` - Logout and blacklist token

### Student Endpoints
- `GET /api/students/students/` - List all students
- `POST /api/students/students/` - Create student
- `GET /api/students/students/{id}/` - Get student details
- `PUT /api/students/students/{id}/` - Update student
- `DELETE /api/students/students/{id}/` - Delete student
- `GET /api/students/students/search/?q={query}` - Search students
- `POST /api/students/students/send_bulk_email/` - Send bulk email (Admin)

### College Endpoints
- `GET /api/students/colleges/` - List all colleges
- `POST /api/students/colleges/` - Create college (Admin)
- `GET /api/students/colleges/{id}/` - Get college details
- `GET /api/students/colleges/{id}/branches/` - Get college branches
- `GET /api/students/colleges/{id}/courses/` - Get college courses
- `GET /api/students/colleges/{id}/students/` - Get college students

### Branch Endpoints
- `GET /api/students/branches/` - List all branches
- `POST /api/students/branches/` - Create branch (Admin)
- `GET /api/students/branches/{id}/courses/` - Get branch courses

### Course Endpoints
- `GET /api/students/courses/` - List all courses
- `POST /api/students/courses/` - Create course (Admin)

## 🔐 Authentication

### Get Access Token

```bash
POST /api/auth/register/
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123",
  "password2": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

Response:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Use Token in Requests

```bash
GET /api/students/students/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## 📝 Example Requests

### Create a Student

```bash
POST /api/students/students/
Authorization: Bearer <token>
Content-Type: application/json

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

## 🧪 Testing Tools

### Using cURL

```bash
# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Get Students
curl -X GET http://127.0.0.1:8000/api/students/students/ \
  -H "Authorization: Bearer <token>"
```

### Using HTTPie

```bash
# Login
http POST http://127.0.0.1:8000/api/auth/login/ \
  email=user@example.com password=password

# Get Students
http GET http://127.0.0.1:8000/api/students/students/ \
  "Authorization: Bearer <token>"
```

### Using Python Requests

```python
import requests

# Login
response = requests.post(
    'http://127.0.0.1:8000/api/auth/login/',
    json={'email': 'user@example.com', 'password': 'password'}
)
token = response.json()['access']

# Get Students
response = requests.get(
    'http://127.0.0.1:8000/api/students/students/',
    headers={'Authorization': f'Bearer {token}'}
)
students = response.json()
```

## 📊 Response Format

### Success Response (List)

```json
{
  "count": 100,
  "next": "http://api.example.com/students/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "student_id": "STU001",
      "college_name": "Example College",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### Error Response

```json
{
  "error": "Authentication credentials were not provided.",
  "detail": "Please provide valid JWT token"
}
```

## 🔧 Features

### Pagination
- Default page size: 10
- Max page size: 100
- Query params: `?page=1&page_size=20`

### Filtering
- Filter by fields: `?college=1&branch=2`
- Search: `?search=john`
- Ordering: `?ordering=-created_at`

### Email Notifications
- Automatic welcome email on student registration
- Update notifications
- Bulk email capability for admins

## 📚 Additional Resources

- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Root**: http://127.0.0.1:8000/api/
- **Postman Collection**: `Student_Management_API.postman_collection.json`
- **Email Setup Guide**: `apps/students/EMAIL_SETUP_GUIDE.md`
- **Quick Start Guide**: `QUICK_START.md`

## 🆘 Support

For issues or questions:
- Check the live documentation at http://127.0.0.1:8000/
- Review logs: `backend/logs/django.log`
- Run system check: `python manage.py check`

## 🔒 Security Notes

- Always use HTTPS in production
- Store tokens securely
- Implement rate limiting
- Validate all inputs
- Use environment variables for secrets
- Enable CORS only for trusted domains

---

**Happy Coding! 🚀**
